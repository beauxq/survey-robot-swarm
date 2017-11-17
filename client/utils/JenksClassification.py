# implementation of Jenks natural breaks classification method
# from: https://gist.github.com/drewda/1299198


def get_jenks_breaks(data_list, num_class):
    data_list = data_list[:]  # copy
    data_list.sort()
    mat1 = []
    for i in range(0, len(data_list) + 1):
        temp = []
        for j in range(0, num_class + 1):
            temp.append(0)
        mat1.append(temp)
    mat2 = []
    for i in range(0, len(data_list) + 1):
        temp = []
        for j in range(0, num_class + 1):
            temp.append(0)
        mat2.append(temp)
    for i in range(1, num_class + 1):
        mat1[1][i] = 1
        mat2[1][i] = 0
        for j in range(2, len(data_list) + 1):
            mat2[j][i] = float('inf')
    v = 0.0
    for l in range(2, len(data_list) + 1):
        s1 = 0.0
        s2 = 0.0
        w = 0.0
        for m in range(1, l + 1):
            i3 = l - m + 1
            val = float(data_list[i3 - 1])
            s2 += val * val
            s1 += val
            w += 1
            v = s2 - (s1 * s1) / w
            i4 = i3 - 1
            if i4 != 0:
                for j in range(2, num_class + 1):
                    if mat2[l][j] >= (v + mat2[i4][j - 1]):
                        mat1[l][j] = i3
                        mat2[l][j] = v + mat2[i4][j - 1]
        mat1[l][1] = 1
        mat2[l][1] = v
    k = len(data_list)
    class_boundaries = []
    for i in range(0, num_class + 1):
        class_boundaries.append(0)
    class_boundaries[num_class] = float(data_list[len(data_list) - 1])
    count_num = num_class
    while count_num >= 2:  # print "rank = " + str(mat1[k][count_num])
        i_d = int((mat1[k][count_num]) - 2)
        # print "val = " + str(dataList[id])
        class_boundaries[count_num - 1] = data_list[i_d]
        k = int((mat1[k][count_num] - 1))
        count_num -= 1
    return class_boundaries
