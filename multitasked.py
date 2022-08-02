from soji_module import main
import multiprocessing

process1 = multiprocessing.Process(target=main(src=1))
process2 = multiprocessing.Process(target=main(src=0))

if __name__ == '__main__':
    process1.start()
    process2.start()
    process1.join()
    process2.join(

    )