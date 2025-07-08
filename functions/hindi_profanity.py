import Levenshtein
with open("functions/hindi_slang.csv","r") as slang_file:
    words = slang_file.read()
words = list(words.split(","))
words = [i.strip().lower() for i in words]

words = (list(set(words)))

def isHindiSlang(user_word:str, threshold:float=0.9)->bool:
    max_ = 0
    for word in words:
        similarity = Levenshtein.ratio(user_word.lower(), word)
        max_ = max(similarity, max_)
        # print(f"word = {word} and similarity = {similarity}, max = {max_}")
    if max_>threshold:
        if max_<1:
            with open("functions/hindi_slang.csv","a") as slang_file:
                slang_file.write(f",{user_word}")
            print("New word added")
        return True
    return False

def containsHindiSlang(content:str, threshold:float=0.9)->bool:
    words = content.split(" ")
    for word in words:
        if isHindiSlang(word, threshold):
            return True
    return False

if __name__=="__main__":
    import time
    myword = input("-->")
    threshold = 0.9
    start = time.time()
    print(isHindiSlang(myword,threshold))
    end = time.time()
    # print(end-start)