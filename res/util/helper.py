import re, asyncio

class Helper:

    # Converts a time string of format 00:00:00 / 00:00 / 00 to int seconds
    async def time_str_to_sec(self, time_str):

        time = None

        if time_str and re.match(r'(?<!.)((?:\d\d?)(?::\d\d){0,2})(?!.)', time_str):
            '''
            times = map(int, re.split(r"[:,]", t))
            print t, times[0]*3600+times[1]*60+times[2]+times[3]/1000k
            '''

            if re.match(r'..:..:..', time_str):
                h = int(time_str[0:2])
                m = int(time_str[3:5])
                s = int(time_str[6:8])
                time = h*3600 + m*60 + s
            elif re.match(r'..:..', time_str):
                m = int(time_str[0:2])
                s = int(time_str[3:5])
                time = m*60 + s
            else:
                time = int(time_str)

        return time


    # Converts seconds to a string with format 00:00:00
    async def time_sec_to_str(self, seconds):
        if seconds is not None:
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            return "%02d:%02d:%02d" % (h, m, s)



    # Converts a hexcolor string (#123Abc) to a list of int rgb values
    async def hex_to_rgb(self, color_hex):
        r_hex = color_hex[1:3]
        g_hex = color_hex[3:5]
        b_hex = color_hex[5:7]

        r_rgb = int(r_hex, 16)
        g_rgb = int(g_hex, 16)
        b_rgb = int(b_hex, 16)

        return [r_rgb, g_rgb, b_rgb]
