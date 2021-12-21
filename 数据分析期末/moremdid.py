import requests
from functools import cache

@cache
def moremdid(n):
    '''
    读取本地的mdidlist.txt文件中的mdid，接着探索更多可能的mdid
    input n【int】
    output 所有已知合法的mdid【list】
    '''

    # 读取文件中的mdidlist
    with open('mdidlist.txt', mode='r') as f:
        mdid = list(map(lambda x: eval(x[:-1]), f.readlines()))
        f.close()
    l_valid = []
    start = mdid[-1] + 1
    for i in range(start, start + n):
        if requests.get(f'https://www.bilibili.com/bangumi/media/md{i}'):
            l_valid.append(i)
    mdid += l_valid
    print(mdid[-10:])
    # 覆盖写，更新源文件中的mdidlist
    with open('mdidlist.txt', mode='w') as f:
        f.writelines(map(lambda x: str(x) + '\n', mdid))
        f.close()
    print(f'completed, length of mdid now is {len(mdid)}')
    return mdid


if __name__ == '__main__':
    for t in range(2):
        moremdid(1000)
        print(f'{t} comleted!')