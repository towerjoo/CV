#coding: utf-8
def gen(lang="Chinese"):
    cell = 36185409382 >> 1
    src = "%s.md" % lang
    fh = open(src)
    cont = fh.read()
    fh.close()
    if lang == "Chinese":
        mark = "男"
        del_mark = "* 这个repo"
    elif lang == "English":
        mark = "Male"
        del_mark = "* This repo"
    cont = cont.replace(mark, "%s, %s" % (mark, str(cell)))
    del_words = cont[cont.index(del_mark):cont.index("<sub>")]
    cont = cont.replace(del_words, "")
    fh = open("%s_ZhuTao.txt" % lang, "w")
    fh.write(cont)
    fh.close()

if __name__ == "__main__":
    gen("Chinese")
    gen("English")
    


