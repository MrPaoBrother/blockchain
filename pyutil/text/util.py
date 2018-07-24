# -*- coding:utf8 -*-


def smart_decode(body, with_detail=False):
    encoding_candidates = ('utf-8', 'gbk', 'big5')
    best_encoding, best_result, best_result_bad_num = '', '', 99999
    for c in encoding_candidates:
        u = body.decode(c, 'replace')
        if c == 'utf-8': # 当编码为utf-8时, body本身可能含有�字符, 计算bad_num要减去body在decode前已经有的�字符.
            bad_num = u.count(u'\uFFFD') - body.count(u'\uFFFD'.encode(c))
        else:
            bad_num = u.count(u'\uFFFD')
        if bad_num < best_result_bad_num:
            best_encoding, best_result, best_result_bad_num = c, u, bad_num
        if bad_num == 0:
            break
    if best_result_bad_num >= 100 or best_result_bad_num * 100 / len(best_result) > 40:
        best_result = u''
    else:
        best_result = best_result.replace(u'\uFFFD', '')

    if with_detail:
        return best_result, best_encoding, best_result_bad_num
    else:
        return best_result