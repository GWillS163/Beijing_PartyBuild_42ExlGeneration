from PIL import Image

def make_regalur_image(img, size=(256, 256)):
    return img.resize(size).convert('RGB')

def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)

def calc_similar(li, ri):
    return hist_similar(li.histogram(), ri.histogram())

def Compare(benchmarkimg,img):
    img1 = Image.open(benchmarkimg)
    img1 = make_regalur_image(img1)
    img2 = Image.open(img)
    img2 = make_regalur_image(img2)
    Confidence =round(calc_similar(img1, img2),5)
    print('-<<[置 信 度]>>--\t\t' + str(Confidence),end='')
    return Confidence
'''-------------------------------------------------------------------'''# 图片对比 图片相似度比较
class Old_Compare():

    # 计算图片hash值
    def get_hash(img):
        img = img.resize((16, 16), Image.ANTIALIAS).convert('L')  # 抗锯齿 灰度
        avg = sum(list(img.getdata())) / 256  # 计算像素平均值
        s = ''.join(map(lambda i: '0' if i < avg else '1', img.getdata()))  # 每个像素进行比对,大于avg为1,反之为0
        return ''.join(map(lambda j: '%x' % int(s[j:j + 4], 2), range(0, 256, 4)))

    # 比较图片hash值
    def hamming(hash1, hash2, n=20):
        b = False
        assert len(hash1) == len(hash2)
        if sum(ch1 != ch2 for ch1, ch2 in zip(hash1, hash2)) < n:
            b = True
        return b

    def bidui(im2):
        global path,benchmark
        im1 = Image.open(path + "\\" + benchmark)  # guest_benchmark
        im2 = Image.open(im2)
        print('-<<[正在图像比对]>>--\t\t',end='')
        c = Compare.hamming(Compare.get_hash(im1), Compare.get_hash(im2), 5)
        print(c)
        return c

if __name__ == '__main__':#Compare(benchmarkimg, img)
    Compare('.\\QYTang_SalesQQ_dete\\benchmark.jpg','.\QYTang_SalesQQ_dete\indiff2.jpg')


