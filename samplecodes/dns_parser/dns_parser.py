#!/usr/bin/env python
#coding: utf-8
class BaseHandler(object):
    """as a contract for child class to obey
    """
    def __init__(self):
        pass

    def read_content(self, *args, **kwargs):
        raise NotImplementedError()

    def write_content(self, *args, **kwargs):
        raise NotImplementedError()

class FileHandler(BaseHandler):
    """File Hanlder for reading and writing
    """
    def read_content(self, *args, **kwargs):
        assert "infile" in kwargs, "need infile parameter"
        fh = open(kwargs.get("infile"))
        cont = fh.read()
        fh.close()
        return cont

    def write_content(self, *args, **kwargs):
        assert "outfile" in kwargs, "need infile parameter"
        assert "content" in kwargs, "need content parameter"
        fh = open(kwargs.get("outfile"), "w")
        fh.write(kwargs.get("content"))
        fh.close()
    
class BaseParser(object):
    """Parser base class(abstract)
    """
    def __init__(self, handler):
        self.handler = handler

    def do_parse(self, cont):
        """The real parse logic goes here
        for each specific parser as child class
        """
        raise NotImplementedError()

    def parse(self, *args, **kwargs):
        in_content = self.handler.read_content(*args, **kwargs)
        out_content = self.do_parse(in_content)
        kwargs.update({
            "content" : out_content,
        })
        self.handler.write_content(*args, **kwargs)


class GrepBasedParser(BaseParser):
    pass
        

class DnsSampleParser(GrepBasedParser):
    def do_parse(self, cont):
        out = ""
        lines = cont.split("\n")
        i = 0
        for line in lines:
            i += 1
            line = line.strip()
            parts = line.split(" ")
            parts = [p for p in parts if p != ""]
            newline = ""

            def parse_domain(part):
                domain = part
                import re
                domain = re.sub("(\([0-9]+\))", ".", domain)
                domain = domain[1:-1]
                host = domain.split(".")[-2:]
                host = ".".join(host)
                return domain, host

            if len(parts) == 15 and parts[0].isdigit():
                domain, host = parse_domain(parts[14])
                newline = "%s %s,%s,%s,%s,,%s,%s,%s,%s,%s,%s,%s\n"  \
                     % (parts[0], parts[1], parts[5], parts[6], parts[7],
                    parts[9], parts[10], parts[11], parts[12], parts[13], domain, host)
            elif len(parts) == 16 and parts[0].isdigit():
                domain, host = parse_domain(parts[15])
                newline = "%s %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"  \
                     % (parts[0], parts[1], parts[5], parts[6], parts[7], parts[9],
                    parts[10], parts[11], parts[12], parts[13], parts[14], domain, host)
            out += newline
        return out

def args_handler():
    import argparse
    parser = argparse.ArgumentParser(description='Parse DNS records')
    parser.add_argument('-i', "--infile", dest="infile", 
                       help='infile to parse')
    parser.add_argument('-o', "--outfile", dest="outfile", 
                       help='outfile to write')
    args = parser.parse_args()
    if args.infile and args.outfile:
        return args.infile, args.outfile
    parser.print_help()
    import sys
    sys.exit(0)


                
if __name__ == "__main__":
    infile, outfile = args_handler()
    handler = FileHandler()
    parser = DnsSampleParser(handler)
    parser.parse(infile=infile, outfile=outfile)
