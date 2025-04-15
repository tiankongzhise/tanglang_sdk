from src.tl_sdk.main import main



if __name__ == "__main__":
    print('请输入c或r,c为线索表,r为预约表')
    func_type = input()
    main(func_type=func_type)
