#!/usr/bin/python
# -*-coding:utf-8-*-

import os
import re

__author__ = 'zwx'
__date__ = '2017.08'


def split_camel(str):
    '''
    将驼峰法单词分成拆分成独立的单词
    :param str: eg: getUserInfo
    :return:    eg: ['get','user','info']
    '''
    if str is None or str == '':
        return []
    i, front = 1, 0
    lst = []
    while i < len(str):
        if str[i].isupper():
            lst.append(str[front:i])
            front = i
        i += 1
    lst.append(str[front:])
    return lst


def replace_holder(content, key_holder, replace_list):
    '''
    单词替换，一对一将key_holder中的单词换成replace_list中的单词
    :param content:     待处理文本
    :param key_holder:  占位符
    :param replace_list: 对应替换单词
    :return: 处理后的文本
    '''

    if len(key_holder) != len(replace_list):
        print('wrong params, len not equal each other')
        return
    if isinstance(content, str):
        for i in range(0, len(key_holder)):
            content = content.replace(key_holder[i], replace_list[i])
    elif isinstance(content, list):
        content = [replace_holder(l, key_holder, replace_list) for l in content]
    return content


def insert_all(path, re_list, lines_list):
    '''
    通过re_list中的正则表达式，匹配到代码块开始位置，并在代码块结束的位置插入lines
    :param path:    待操作文件绝对路径
    :param re_list: regex列表
    :param lines_list: line的二维数组
    :return: None
    '''

    if not os.path.exists(path):
        print('%s not exists' % path)
        return
    f = open(path, 'r+', encoding='utf-8')
    lines = f.readlines()
    f.seek(0)
    content = f.read()
    f.truncate()
    f.seek(0)
    line_index_to_insert = {}
    for i in range(0, len(lines)):
        l = lines[i]
        if i in line_index_to_insert.keys():
            lst = line_index_to_insert[i]
            for repl in lst:
                f.write(repl)
        f.write(l)
        for i in range(0, len(re_list)):

            if isinstance(lines_list[i], list):
                lst = []
                all_before = -1
                if re.match(re_list[i], l):
                    for item in lines_list[i]:
                        if item.strip() not in content:
                            start = content.index(l) + len(l)
                            end = find_line_before_parentheses(content, start)
                            all_before = content[:end + 1].count('\n')
                            lst.append(item)
                line_index_to_insert[(all_before)] = lst

            else:
                if re.match(re_list[i], l):
                    if lines_list[i].strip() not in content:
                        f.write(lines_list[i])
    f.close()


def find_parentheses(strs, start):
    '''
    寻找当前代码块位置，对应的结束位置的'}'的位置
    :param strs: 查找的代码块
    :param start: 当前位置
    :return: 当前位置对应的结束'}'的位置。这里假设代码格式良好，'{'、'}'成对出现。找不到返回-1
    '''
    depth = 1
    curr = start
    while curr < len(strs):
        if strs[curr] == '{':
            depth += 1
        elif strs[curr] == '}':
            depth -= 1
        if depth == 0:
            return curr
        curr += 1
    return depth


def find_line_before_parentheses(strs, start):
    '''
    找到从start起，对应结束位置的'}'的前一个换行符位置
    :param strs:
    :param start:
    :return:
    '''
    pos = -1
    end = find_parentheses(strs, start)
    if end != -1:
        pos = strs.rfind('\n', start, end)
    return pos
