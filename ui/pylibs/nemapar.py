
import time

class NMEAParser:
    def __init__(self):

        self.last_known_fix = {}

    def feed(self, data):
        if not data:
            return
        lines = data.splitlines()
        for line in lines:
            parsed = self._parse_line(line.decode('utf-8'))

            self.last_known_fix.update(parsed)

    def _parse_line(self, s):
        out = {'raw': s, 'valid': False, 'type': None, 'has_fix': False}
        if not s.startswith('$'):
            return out

        star = s.find('*')
        if star != -1 and star+3 <= len(s):
            given = int(s[star+1:star+3], 16)
            cs = 0
            for ch in s[1:star]:
                cs ^= ord(ch)
            out['valid'] = (cs == given)
            if not out['valid']:
                return out
            body = s[1:star]
        else:
            return out

        fields = body.split(',')
        header = fields[0]
        stype = header[-3:]
        out['type'] = stype

        if stype == 'GGA':
            out.update(self._parse_gga(fields))
        elif stype == 'RMC':
            out.update(self._parse_rmc(fields))
        elif stype == 'GSA':
            out.update(self._parse_gsa(fields))
        elif stype == 'GSV':
            out.update(self._parse_gsv(fields))
        else:

            out['fields'] = fields[1:]

        ns = out.get('num_satellites')
        if ns == '':
            out['num_satellites'] = 0
        return out

    def _nmea_to_decimal(self, val, hemi):
        if not val:
            return None
        try:

            dot = val.find('.')
            if dot == -1:
                dot = len(val)

            deg_len = dot - 2
            if deg_len <= 0:
                return None
            deg = int(val[:deg_len])
            minutes = float(val[deg_len:])
            dec = deg + minutes / 60.0
            if hemi in ('S', 'W'):
                dec = -dec
            return dec
        except Exception:
            return None

    def _parse_time(self, t):
        if not t:
            return None
        try:
            hh = int(t[0:2])
            mm = int(t[2:4])
            ss = int(t[4:6])
            frac = 0.0
            if '.' in t:
                frac = float('0.' + t.split('.', 1)[1])
            return {'hour': hh, 'minute': mm, 'second': ss, 'fraction': frac}
        except:
            return None

    def _parse_date(self, d):
        if not d or len(d) < 6:
            return None
        try:
            day = int(d[0:2])
            month = int(d[2:4])
            year = int(d[4:6]) + 2000
            return {'day': day, 'month': month, 'year': year}
        except:
            return None

    def _parse_gga(self, f):

        out = {}
        out['time'] = self._parse_time(f[1])
        out['latitude'] = self._nmea_to_decimal(f[2], f[3])
        out['longitude'] = self._nmea_to_decimal(f[4], f[5])
        out['fix_quality'] = f[6]

        out['num_satellites'] = f[7]
        out['hdop'] = f[8]
        out['altitude'] = f[9]
        return out

    def _parse_rmc(self, f):
        out = {}
        out['time'] = self._parse_time(f[1])
        out['status'] = f[2]
        out['latitude'] = self._nmea_to_decimal(f[3], f[4])
        out['longitude'] = self._nmea_to_decimal(f[5], f[6])
        out['speed_knots'] = f[7]
        out['course_deg'] = f[8]
        out['date'] = self._parse_date(f[9])
        out['mag_var'] = f[10]
        out['mag_var_dir'] = f[11]
        return out

    def _parse_gsa(self, f):
        out = {}
        out['mode'] = f[1]
        out['fix_type'] = f[2]
        sats = []
        for i in range(3, 15):
            if f[i] != '':
                sats.append(f[i])
        out['sv_used'] = sats
        out['pdop'] = f[15]
        out['hdop'] = f[16]
        out['vdop'] = f[17]

        out['num_satellites'] = len(sats)
        return out

    def _parse_gsv(self, f):
        out = {}
        out['num_messages'] = f[1]
        out['message_number'] = int(f[2])
        out['sats_in_view'] = int(f[3])

        if out['sats_in_view'] == 0:
            out['sats'] = []
            out['num_satellites'] = 0
            return out

        sats = []
        for i in range(4, len(f), 4):
            prn = f[i]
            elev = f[i+1]
            az = f[i+2]
            cnr = f[i+3]
            sats.append({'prn': prn, 'elev': elev, 'az': az, 'cnr': cnr})
        out['sats'] = sats
        out['num_satellites'] = len(sats)
        return out
