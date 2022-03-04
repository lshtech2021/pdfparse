import sys, os
import fitz

def extract_taxe(data):
    taxe = {}
    for block in data['blocks']:
        success, result = parse_blocks(block)
        if success:
            for key in result:
                taxe[key] = result[key]
    return taxe

def parse_blocks(block):
    result = {}
    success = False
    if "lines" in block:
        lines = block["lines"]
        count = len(lines)
        i = 0
        while(i<count):
            line = lines[i]
            find, field_text = parse_line(line)
            if find and field_text in ["TPS", "TVQ"]:
                # print(field_text)
                i += 1
                line = lines[i]
                field_value = line["spans"][0]["text"]
                # print(field_value)
                if field_value:
                    success = True
                    result[field_text] = field_value
            i += 1
    return success, result

def parse_line(line):
    spans = line["spans"]
    find = False
    for span in spans:
        if span["text"] in ["TPS", "TVQ"]:
            find = True
            break
    return find, span["text"]

def main(argv):
    file = argv[1]
    with fitz.open(file) as doc:
        page = doc[0]
        data = page.get_text("dict")
        taxe = extract_taxe(data)
        print(taxe)

if __name__=='__main__':
    main(sys.argv)
