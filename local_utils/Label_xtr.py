def getLabelsFromTxt(path="coco-lbl.txt", verbose=True):
    with open(path, "r") as lbls:  # Open txt file
        a = lbls.read()  # Read txt file
        b = a.split('\n')  # Split by every line into list
        if verbose: print("Labels Extracted: ", b)  # print extracted list
        return b

def getLabelsFromYaml(path="data.yaml", verbose=True):  # generally the same but with a yaml file
    import yaml
    with open(path, 'r') as file:
        a = yaml.full_load(file)["names"]
    if verbose: print(a)
    return a

if __name__=="__main__":
    getLabelsFromTxt()