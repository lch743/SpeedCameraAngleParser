# Author = 'LiuLeo2'
import sys
import getopt
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2


def calc_angle_by_pnt(pnt_start_lat, pnt_start_lon, pnt_end_lat, pnt_end_lon):
    import math
    angle = math.atan2(pnt_end_lat - pnt_start_lat, pnt_end_lon - pnt_start_lon)
    if angle < 0:
        angle += 2 * math.pi
    angle *= 57.29577951308232
    if 0 <= angle < 90:
        angle = 90 - angle
    elif 90 <= angle < 180:
        angle = 360 - (angle - 90)
    elif 180 <= angle < 270:
        angle = 180 + (270 - angle)
    elif 270 <= angle < 360:
        angle = 90 + 360 - angle
    return angle


def calc_distance_by_pnt(lat_left, lon_left, lat_right, lon_right):
    import math
    r = 6378137.0
    lat_left_rad = lat_left * math.pi / 180
    lon_left_rad = lon_left * math.pi / 180
    lat_right_rad = lat_right * math.pi / 180
    lon_right_rad = lon_right * math.pi / 180
    dlon = abs(lon_left_rad - lon_right_rad)
    dlat = abs(lat_left_rad - lat_right_rad)
    p = pow(math.sin(dlon / 2), 2) + math.cos(lon_left_rad) * math.cos(lon_right_rad) * pow(math.sin(dlat / 2), 2)
    d = r * 2 * math.asin(math.sqrt(p))
    return d

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "i:s:")
    in_file_name = ''
    split_char = ''
    if len(opts) <> 2:
        print 'Arguments Num Error!'
    else:
        for opt, value in opts:
            if opt == '-i':
                in_file_name = value
            elif opt == '-s':
                split_char = value
    record = []
    records = []
    urls = []
    key = 'AIzaSyCkF6hNZLbw_FIU_02oRnBPPjJidLm5SIc'
    if len(in_file_name) != 0:
        with open(in_file_name, 'r') as fin:
            for line in fin:
                line = line.rstrip('\n')
                line = line.rstrip('\r')
                record = line.split(split_char)
                records.append(line)
                if record[0] == 'lat' and record[1] == 'lon':
                    continue
                lat = str(int(record[1]) / 1000000.0)
                lon = str(int(record[2]) / 1000000.0)
                text = record[5]
                index = text.find(' towards ') + len(' towards ')
                destination = urllib2.quote(text[index:] + '+in+singapore')
                #origin = urllib2.quote(text[:index] + '+in+singapore')
                origin = urllib2.quote(lat + ' ' + lon)
                urls.append("https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&key=%s&language=eng" % (origin, destination, key))

        with open(in_file_name, 'w') as fout:
            d_mark = 20
            import symbol
            import json
            for i in range(len(urls)):
                page = urllib2.urlopen(urls[i])
                json_parse = json.load(page)
                instructions = json_parse["routes"][0]["legs"][0]['steps'][0]["html_instructions"]
                start_lat = json_parse["routes"][0]["legs"][0]['start_location']['lat']
                start_lon = json_parse["routes"][0]["legs"][0]['start_location']['lng']
                end_lat = json_parse["routes"][0]["legs"][0]['end_location']['lat']
                end_lon = json_parse["routes"][0]["legs"][0]['end_location']['lng']
                angle = calc_angle_by_pnt(start_lat, start_lon, end_lat, end_lon)
                records[i] = records[i][:records[i].rfind(split_char)] + split_char + str(int(angle + 0.5))
            for line in records:
                fout.write(line + '\n')
