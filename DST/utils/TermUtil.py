import re


def filterTerm(term):
    try:
        term.encode(encoding="ascii")
    except:
        return False

    if len(term) == 1 and term != "r" and term != "c":
        return False
    if term[-1] == "." or term[-1] == "_":
        return False
    # the term cannot include these punctuations
    special_list = ["@", "*", "[", "]", "=", ">", "<", "\\", "/", "|", "&", "$", "~", "^", "%", "..", "--", "__", "`",
                    "´", "’", "‘", "“", "”", " ", "£", "¿", "www.", ".com", "test.", "slow", "'s", ".org", ".axd",
                    ".app",
                    ".mail", ".test", ".mf", ".location",
                    ".system", ".imageio", ".io", ".beginform", ".futures", ".mappath", ".drawing", ".observablearray",
                    ".conf", ".table",
                    ".path", ".actionlink", ".settings", ".log", ".util", ".concurrent"]
    for i in special_list:
        if i in term:
            return False
            return False
    # remove terms whose begining is
    firstLetter_set = set(["#", "_", "+", "-"])
    if term[0] in firstLetter_set:
        return False
    # remove terms whose first character is a digit except some special cases
    if len(re.findall(r"\d\.\d", term)) > 0:  # no version number such as "3.2.1"
        return False

    signal = False  # fail if there are no letters in the term
    for character in term:
        if character.isalpha():
            signal = True
            break
    return signal
