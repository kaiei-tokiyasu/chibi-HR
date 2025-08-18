class ui:
    seperator = None
    def __init__(self, title= None, body = None):
        self.title = title
        self.body = body
        return
    
    def print_title(self):
        headTitle = f"||=== {self.title} ===||"
        seperator = "=" * len(headTitle)
        print(seperator)
        print(headTitle)
        print(seperator)

    def print_body(self):
        if self.body is None: 
            return
        headTitle = f"||=== {self.title} ===||"
        seperator = "=" * len(headTitle)
        bodydesc = f"{self.body}"
        print("")
        print(bodydesc)
        print("")
        print(seperator)
    
    def setUi(self, title=None, desc=None):
        self.title = title
        self.body = desc
