#coding: utf8

__version__ = '0.0.1'

"""

    xxtea implemented in python (非标准)
    Based on https://github.com/lyxint/xxtea
    Modified by pure (利用ctypes解决与java移位运算的结果不兼容问题)

"""
import itertools
from ctypes import c_longlong


def str2longs(s):
    length = (len(s) + 7) / 8
    s = s.ljust(length * 8, '\0')
    result = []
    for i in xrange(length):
        j = 0
        j |= ord(s[i * 8])
        j |= ord(s[i * 8 + 1]) << 8
        j |= ord(s[i * 8 + 2]) << 16
        j |= ord(s[i * 8 + 3]) << 24
        j |= ord(s[i * 8 + 4]) << 32
        j |= ord(s[i * 8 + 5]) << 40
        j |= ord(s[i * 8 + 6]) << 48
        j |= ord(s[i * 8 + 7]) << 56
        result.append(c_longlong(j))
    return result


def longs2hexstr(s):
    """
    similar to "Long.toHexString" in Java
    """
    result = ""
    for c in s:
        if c.value < 0L:
            temc = c.value + 2 ** 64
        else:
            temc = c.value
        tem = hex(temc).replace('0x', '').strip('L')
        tem = _padleft(16, tem, '0')
        result += tem
    return result


def hexstr2longs(s):
    result = []
    length = len(s) / 16
    for i in xrange(length):
        result.append(c_longlong(long(s[i * 16:16 + i * 16], 16)))
    return result


def longs2str(s):
    result = ""
    for c in s:
        result += chr(c.value & 0xFF) + chr(c.value >> 8 & 0xFF) + chr(c.value >> 16 & 0xFF) \
                  + chr(c.value >> 24 & 0xFF) + chr(c.value >> 32 & 0xFF) + chr(c.value >> 40 & 0xFF) \
                  + chr(c.value >> 48 & 0xFF) + chr(c.value >> 56 & 0xFF)
    return result.rstrip('\0')


def btea(v, k, decode=False):
    if decode:
        n = -len(v)
    else:
        n = len(v)
    if not isinstance(v, list) or \
            not isinstance(n, int) or \
            not isinstance(k, (list, tuple)):
        return False

    # MX = lambda: ((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4)) ^ (sum ^ y) + (k[(p & 3) ^ e] ^ z)
    MX = lambda: ((z.value >> 5) ^ (t1.value)) + ((y.value >> 3) ^ (t2.value)) ^ (sum.value ^ y.value) + (
        k[int((p & 3) ^ e)].value ^ z.value)
    u32 = lambda x: x

    sum, t1, t2, y, z = c_longlong(0), c_longlong(0), c_longlong(0), c_longlong(0), c_longlong(0)
    y.value = v[0].value
    DELTA = 0x9e3779b9
    #    DELTA = 2654435769L
    if n > 1:
        z.value = v[n - 1].value
        q = 6 + 52 / n
        while q > 0:
            q -= 1
            sum.value = sum.value + DELTA
            e = (sum.value >> 2) & 3
            p = 0
            while p < n - 1:
                y.value = v[p + 1].value
                t1.value = y.value << 2
                t2.value = z.value << 4
                z.value = v[p].value = v[p].value + MX()
                p += 1
            y.value = v[0].value
            t1.value = y.value << 2
            t2.value = z.value << 4
            z.value = v[n - 1].value = u32(v[n - 1].value + MX())
        return True
    elif n < -1:
        n = -n
        q = 6 + 52 / n
        sum.value = q * DELTA
        while sum.value != 0:
            e = (sum.value >> 2) & 3
            p = n - 1
            while p > 0:
                z.value = v[p - 1].value
                t1.value = y.value << 2
                t2.value = z.value << 4
                y.value = v[p].value = (v[p].value - MX())
                p -= 1
            z.value = v[n - 1].value
            t1.value = y.value << 2
            t2.value = z.value << 4
            y.value = v[0].value = (v[0].value - MX())
            sum.value -= DELTA
        return True
    return False


def safestr(obj, encoding='utf-8'):
    r"""
    Converts any given object to utf-8 encoded string.

        >>> safestr('hello')
        'hello'
        >>> safestr(u'\u1234')
        '\xe1\x88\xb4'
        >>> safestr(2)
        '2'
    """
    if isinstance(obj, unicode):
        return obj.encode(encoding)
    elif isinstance(obj, str):
        return obj
    elif hasattr(obj, 'next'): # iterator
        return itertools.imap(safestr, obj)
    else:
        return str(obj)


def _padright(width, ss, special_char='\0'):
    return ss.ljust(width, special_char)


def _padleft(width, ss, special_char='\0'):
    return ss.rjust(width, special_char)


def encrypt(data, key):
    min_width = 32
    data = _padright(min_width, data)
    key = _padright(min_width, key)
    data = safestr(data)
    key = safestr(key)
    v = str2longs(data)
    k = str2longs(key)
    btea(v, k)
    result = longs2hexstr(v)
    return result


def decrypt(enc, key):
    """
    enc: encoded strings
    key: key
    return: decoded strings (unicode strings)
    """
    key = _padright(32, key)
    v = hexstr2longs(enc)
    k = str2longs(key)
    btea(v, k, decode=True)

    res = longs2str(v)
    return res.decode('utf8')


if __name__ == '__main__':
    # skey = u"hello"
    # sdata = u"截止当前，您的3G赠送流量1G的3G套餐内流量1048576KB,已使用40079KB,剩余1008497KB;WCDMA(3G)-66元基本套餐B的3G语音200分钟,已使用126分钟,剩余74分钟;可视电话10分钟,已使用0分钟,剩余10分钟;3G套餐内流量61440KB,已使用61440KB,剩余0KB;M值6M,已使用0M,剩余6M;T值10T,已使用0T,剩余10T;3G国内流量10元包100M的3G国内流量102400KB,已使用102400KB,剩余0KB;通信费用请以帐详单为准。 【买4G就上10010.com】"
    # encoded = encrypt(sdata, skey)
    # # encoded = "ea28e9690c877eba167693e67b057581e31d7981144642d009d32ed223a15a5dcc2134425ee646fe2a0b273396013d17f4b2bd5b1eef2fd33813d5cd9cc76ce3ed254072fa7bc411864d6ca1dcd528a4767dac6ac7540525c5e1de9e0d100635784b691c02d2e988b575403f8b8ef069b3fb81addac89a3af4a58bcd4ecd20d886aeaaa0535e0fe9dcb7c73f8b32f2a5a35269bdb3fe1598df33794b445fc3362be5fcc9504de9e9e2864cb894b31be9829f1a4450be74a088d559ccfe834821364fd30626a48a73a1969aea1aff3d80c912ea7021e07a84049e7a6c137bcdf629143511f8970de59e6f0c7b876589bd57cd574e2c37cb3847edd4842d71a7f4e25dd667c9d102b96ed9c85133fa69475abfdc0f9248ec2d9e2cd7c3276c0d18ac0f67efc3ca58fa256029724f730c44552e824ef994be216c2e75e383c767d3dd5d5f951bd650230008267b88dfb402dafa33fe9d937bdaa0d59f2c6b2358a13fa96df6d40db887a04f10a2ee74f3a0d29ff49278ee85396712d74e0eefea8278e52117fd8cd26940396a7e03ad1365bde7fb57a22b7860e1a2ab054321e9cfcbccf9e9b10db2cc1ab2de2abbed6e62ba17e650bc7f7f22fef9cbfbfbd7e8b84d9b23ecb738a454c23855b808809d74274b1f74edccb1d76307abef1d7522a167e991af5eb34e76662cd09b0ca9ccdd"
    # decoded = decrypt(encoded, skey)
    # print 'encoded=', len(encoded), encoded
    # print 'decoded=', len(decoded), decoded
    # assert sdata == decoded

    test_en = u'{"province":"北京","isp":"中国移动","brand":"神州行","code":"CXGLL","number":"10086","msg":"您好！截至到2015年03月10日15时28分，您已使用数据流量804.85MB，套餐内剩余流量2267.03MB，其中：国内通用流量剩余1416.58MB，本地流量剩余173.37MB，本地4G流量剩余677.08MB，感谢您使用流量查询服务。查流量，就用“北京移动”手机客户端。点击下载： http://mobilebj.cn/?c=120/ 中国移动"}'
    test_de = '56a5df6b95e5f78e1372ca05c11cd957249732275c94ac91bf98a6342bbb7c8e6948e2c6c013c24f2c91c1953619e086c37a2662ba58413e9124220a8008ce09e6a32c2b43b267f0f71a2b21f692ed5605efe67162d4b8eb03f826482a8b2dccc812a7cf958e8d646e26c76f1ba6cbf3a2c6932cc49fb84af4b12434cf23b5491a2a36f51e8fd59ba047d459196932432684f27e28fb819252e8e9714ba8079d794394577c6ef2f7e5168da97a74726e5fb94d17da3f99951eca7dd7a96613ba8e05f12ad5701b7b496bed7c4963ce4c0bafe2c7c7f9947f480c4b931df036f44d90af3be195b67d347b56f833f4d1af004516066b6c036f6e5f7907ac543d4eb01d2089d1afb6ffa7c407d3d70c458f9b095ad0eff4d2a8c2c6f7ac1aa4c66e57c31436db8ba758e53b112eed1fa6d6703fef467f189f04'
#     print encrypt(test_en, 'OUPENG3609ec3c97c59' + '123')
    print decrypt(test_de, 'OUPENG3609ec3c97c59' + '123')
#     print decrypt('45837d79dad3ec12b6dcbdb263674d62bae1530b6b489b4e6886f9341874125d','OUPENG3609ec3c97c59')

