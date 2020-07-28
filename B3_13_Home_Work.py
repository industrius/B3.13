class TopLevelTag:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.child = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iadd__(self, other):
        self.child.append(other)
        return self
    
    def __str__(self):
        result = f"<{self.tag_name}>\n"
        for item in self.child:
            result += "   {}".format(str(item))
        return result + f"   </{self.tag_name}>\n"


class Tag(TopLevelTag):
    def __init__(self, tag_name, is_single=False, **kwargs):
        self.is_single = is_single
        self.tag_name = tag_name
        self.text = ""
        self.child = []
        self.tag_attr = kwargs

    def __str__(self):
        tag_attr=""
        # разбираем атрибуты, пришедшие через **kwargs
        # сразу формируем строку нужного формата в переменной tag_attr
        for key, val in self.tag_attr.items():
            if isinstance(val, tuple) or isinstance(val, list):
                tag_attr += ('{}="{}" '.format(key.replace("_", "-").replace("klass", "class"), " ".join(val)))
            else:
                tag_attr += ('{}="{}" '.format(key.replace("_", "-").replace("klass", "class"), val))

        if self.child:
            # формируем строку для вывода тэга с атрибутами
            result = "   <{}{}{}>\n".format(self.tag_name, " " if tag_attr else "", tag_attr.strip())
            for item in self.child:
                result += "      {}".format(str(item))
            return result + f"      </{self.tag_name}>\n"
        else:
            if self.is_single: # если тэг однострочный и без вложенных тэгов
                return "   <{}{}{}/>\n".format(self.tag_name, " " if tag_attr else "", tag_attr.strip())
            else:
                return "   <{}{}{}>{}</{}>\n".format(self.tag_name, " " if tag_attr else "", tag_attr.strip(), self.text, self.tag_name)


class HTML(TopLevelTag):
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.child = []

    def __exit__(self, type, value, traceback):
        if self.file_name:
            with open(self.file_name, "w") as f:
                f.write(str(self))
        else:
            print(self)
    
    def __str__(self):
        result = "<html>\n"
        for item in self.child:
            result += "   {}".format(str(item))
        return result + "</html>\n"


with HTML() as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body