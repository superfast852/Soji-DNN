def getLabelsFromTxt(path="coco-lbl.txt", verbose=True):
    with open(path, "r") as lbls:
        a = lbls.read()
        b = a.split('\n')
        if verbose: print("Labels Extracted: ", b)
        return b

def getLabelsFromYaml(path="data.yaml", verbose=True):
    import yaml
    with open(path, 'r') as file:
        a = yaml.full_load(file)["names"]
    if verbose: print(a)
    return a

if __name__=="__main__":
    getLabelsFromTxt()