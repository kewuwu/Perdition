
def get_input(return_type=str, validation=None):
        while True:
            uin = input("> ")
            if uin.lower() in ['q', 'quit', 'exit']:
                exit()
            try:
                uin = return_type(uin)
            except:
                print(f"Invalid input")
                continue
            if validation:
                if validation(uin):
                    return uin
                print("Invalid input")
            else:
                return uin