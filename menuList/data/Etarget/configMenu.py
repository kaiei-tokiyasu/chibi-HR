from config import ConfigManager
from controller.climenu import CLImenu

def dummy():
    return

class TargetConfigMenu:
    def __init__(self):
        self.title = "Target Grading Config Menu"
        
        self.menuList = {
            "1": ("Monthly Grade", lambda: self.bulkView("target-M")),
        }
    def viewMPGrade(self, key_name):
        target = ConfigManager().config['data'][key_name]
        print("Current Passing Grade config")
        print(target)
        u_input = input(f"Edit Current (y/N):")
        print()
        if u_input.lower() == "y":
            GradeList = ["A", "B", "C", "D", "E", "F"]
            while True:
                new_input = input(f"Enter minimum passing grade: ")
                
                try:
                    new_input = new_input.upper()
                    if new_input in GradeList:
                        # print("accepted")
                        is_save = input("Save current Config (Y/n):")

                        if is_save.lower() == "n":
                            print("Operation Cancelled")
                            break
                        
                        ConfigManager().set(section="data", key=key_name, value=new_input)
                        break
                    else:
                        print(f"Invalid Input. must contain {GradeList}")
                except ValueError:
                    print(f"Invalid Input. cannot be numberic")

            new_input.upper()
            
        else:
            print("No Change") 
        return
    def bulkView(self, key_name):
        target = ConfigManager().config['data'][key_name]
        print("Current Grade config")
        print("Hint: Higher value is the best Score")
        for key, value in target.items():
            print(f"{key}: {value}")
        
        u_input = input(f"Edit Current (y/N):")
        print()
        if u_input.lower() == "y":
            self.bulkEdit(key_name=key_name)
        else:
            print("No Change") 

    def getUserInput (self, key, prev, prevKey, initVal):
        while True:
            u_input = input(f"{key}: ")
            try:
                u_input = int(u_input)
                if u_input < 0:
                    print("cannot be negative")
                elif u_input < initVal:
                    print(f"cannot be under {initVal}")
                elif u_input >= prev and prevKey is not None:
                    print(f"cannot be same or more than {prevKey} value ({prev})")
                else:
                    return u_input
            except ValueError:
                print("Invalid input. Please enter a valid non-negative number (no letters or symbols).")

    def bulkEdit(self, key_name):
        target = ConfigManager().config['data'][key_name]

        new_data = {}

        prevkey = None
        initVal = len(target) -1
        prevVal = 0
        for key, _ in target.items():
            user_input = self.getUserInput(key=key, prev=prevVal, prevKey=prevkey, initVal=initVal)
            new_data[key] = user_input
            prevkey = key
            prevVal = user_input
            initVal = user_input - 1
        
        print()

        is_save = input("Save current Config (Y/n):")

        if is_save.lower() == "n":
            print("Operation Cancelled")
            return
        
        self.saveBulk(key_name= key_name, new_data=new_data)
        return
      
    def saveBulk(self, key_name, new_data):
        ConfigManager().set(section="data", key=key_name, value=new_data)

    def run(self):
        title = self.title
        Menu = CLImenu(menuTitle=title) 
        MenuList = self.menuList
        for idx, (label, func) in MenuList.items():
            Menu.add_option(idx, label, func)

        Menu.run()
