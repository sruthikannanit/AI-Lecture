def is_lecture(text, title):
    lecture = ["lecture","tutorial","math","programming","lab","course"]
    non = ["song","music","vlog","movie","comedy"]

    data = (text + " " + title).lower()

    return sum(w in data for w in lecture) > sum(w in data for w in non)