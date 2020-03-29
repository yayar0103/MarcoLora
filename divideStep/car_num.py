import numpy as np

input_signal = np.random.choice(2, 100)
signal = np.insert(input_signal, 0, 0)
start = False
end_num = 0   
start_num = 0
num = 0
for catch in range(signal[:-4].shape[0]):
    i = signal[catch:catch+2]
    # print(str(catch) + ':' + str(signal[catch:catch+2]))
    if i[0] == 0 and i[1] == 1 and start == False:
        start = True
        startt = catch+1
    elif i[0] == 0 and i[1] == 1 and start == True:
        end_num = 0
    elif i[0] == 1 and i[1] == 0 and start == True:
        end_num += 1
        # print('end_num:' + str(end_num))
    elif i[0] == 0 and i[1] == 0 and start == True:
        end_num += 1
        # print('end_num' + str(end_num))         
        if end_num == 4:
            start = False
            start_num = 0
            end_num = 0
            endd = catch+1
            if endd - startt == 4:
                start = False
            else:
                print('start:' + str(startt))
                print('end:' + str(endd-4))
                print("--------")


