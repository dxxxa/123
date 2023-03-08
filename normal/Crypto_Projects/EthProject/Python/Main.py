from Tools import *


def main():
    set_file_name("Output_" + str(strftime("%d-%b_%H-%M-%S", localtime())) + ".txt")
    print(SAMPLE_OUTPUT)
    r_time = get_request_time()
    print(f"Request Time: {r_time}")
    x = input(">>> ")
    if x == "q":
        exit(0)

    elif x == "1":
        os.system('cls')
        print("""\nMyEtherWallet | Check One\n[1] DECimal\n[2] PRIV-Key\n[3] PUB-Key\n\n[b] Back\n[q] Quit\n""")
        y = input(">>> ")
        if y == "q":
            exit(0)
        elif y == "1":
            dec_number = int(input("DECimal :>>> ").strip())
            single_dec(dec_number)
            main()

        elif y == "2":
            private_key = input("PRIV-Key :>>> ").strip()
            public_key, wallets, values, t_res = private_check(private_key)
            print(public_key)
            for i in range(len(wallets)):
                print(wallets[i], values[i])
            print(t_res)
            main()

        elif y == "3":
            public_key = input("PUB-Key :>>> ").strip()
            single_pub(public_key)
            main()
        elif y == "b":
            os.system('cls')
            main()
        else:
            print("Command not Recognized")

    elif x == "2":
        os.system('cls')
        while True:
            list_check()

    elif x == "3":
        os.system('cls')
        range_check(r_time)
        main()
    elif x == "4":
        os.system('cls')
        while True:
            random_check()

    elif x == "5":
        clear_files()
        main()

    else:
        print("Command not Recognized")


if __name__ == '__main__':
    main()
