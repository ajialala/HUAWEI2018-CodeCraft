# -*-coding:utf-8-*-
from time import clock

# 动态规划
def package_dyn(opt_select,flavor_vmnum,flavor_cpu_format,flavor_mem_format,res_cpu,res_mem):
    vm_num = 0
    for value in flavor_vmnum.values():
        vm_num += int(value)
    flavor = ['']*vm_num
    weight = [0]*vm_num
    value = [0]*vm_num
    ik = 0
    if opt_select == 'CPU':
        capacity_weight = res_cpu
        capacity_value = res_mem
        for k, v in flavor_vmnum.items():
            while v>0:
                v = v-1
                flavor[ik] = k
                weight[ik] = flavor_cpu_format[k]
                value[ik] = flavor_mem_format[k]
                ik = ik + 1
    elif opt_select == 'MEM':
        capacity_weight = res_mem
        capacity_value = res_cpu
        for k, v in flavor_vmnum.items():
            while v>0:
                v = v-1
                flavor[ik] = k
                value[ik] = flavor_cpu_format[k]
                weight[ik] = flavor_mem_format[k]
                ik = ik + 1
    result = {}
    phymac_num = 0
    l = len(weight)
    
    while l>0:
        minw = min(weight[0:l])
        sumw = sum(weight[0:l])
        sumv = sum(value[0:l])
        blank = [0] * l
        if capacity_weight < minw:
            return (0,0)                   #blank
        if capacity_weight >= sumw and capacity_value >= sumv:
            phymac_num = phymac_num + 1
            #print phymac_num
            result.setdefault(phymac_num, {})
            for kk in range(0, l):
                if result[phymac_num].has_key(flavor[kk]):
                    result[phymac_num][flavor[kk]] = result[phymac_num][flavor[kk]] + 1
                else:
                    result[phymac_num][flavor[kk]] = 1
            return (phymac_num,result)
        sol = {}
        sem = [0]*l
        # 解字典，sol[限制条件1_限制条件2_前i个flavor]=[最大价值,选择的物品列表]
        # 初始化
        for j in range(0, capacity_weight + 1):
            for js in range(0, capacity_value + 1):
                for i in range(l):
                    sol.setdefault('_'.join([str(j), str(js), str(i)]), [0,0, blank])
        # 只能选第一个物品时，当背包足够大，所能收纳的最大价值为value[0]
        blank2 = blank[:]
        blank2[0] = 1
        for j in range(1, capacity_weight + 1):
            for js in range(1, capacity_value + 1):
                if j >= weight[0] and js>=value[0]:
                    sol['_'.join([str(j),str(js), '0'])] = [weight[0],value[0], blank2]

        for j in range(1, capacity_weight + 1):
            for js in range(1, capacity_value + 1):
                for i in range(1, l):
                    if weight[i] > j or value[i]>js:  # 第i个物品超出背包容量限制
                        sol['_'.join([str(j),str(js), str(i)])] = sol['_'.join([str(j),str(js), str(i - 1)])]
                    else:
                        w1 = sol['_'.join([str(j),str(js), str(i - 1)])][0]
                        w2 = sol['_'.join([str(j - weight[i]),str(js- value[i]), str(i - 1)])][0] + weight[i]
                        v1 = sol['_'.join([str(j), str(js), str(i - 1)])][1]
                        v2 = sol['_'.join([str(j - weight[i]), str(js - value[i]), str(i - 1)])][1] + value[i]
                        if w2<=capacity_weight and v2<=capacity_value and w1 <= w2 and v1<=v2:
                            index = sol['_'.join([str(j - weight[i]),str(js-value[i]), str(i - 1)])][2][:]
                            index[i] = 1
                            sol['_'.join([str(j),str(js), str(i)])] = [w2,v2,index]
                        else:
                            #print 'cd:%d %d %d %d' %(w1,w2,v1,v2)
                            sol['_'.join([str(j),str(js), str(i)])] = sol['_'.join([str(j),str(js), str(i - 1)])]
                            
        #print '%d %d' %(sol['_'.join([str(capacity_weight),str(capacity_value), str(l - 1)])][0],sol['_'.join([str(capacity_weight),str(capacity_value), str(l - 1)])][1])
        sem = sol['_'.join([str(capacity_weight),str(capacity_value), str(l - 1)])][2]
        phymac_num = phymac_num +1
        cm = 0
        #print '%d' %phymac_num
        result.setdefault(phymac_num,{})
        for kk in range(0,l):
            if sem[kk]==1:
                if result[phymac_num].has_key(flavor[kk]):
                    result[phymac_num][flavor[kk]] = result[phymac_num][flavor[kk]] + 1
                else:
                    result[phymac_num][flavor[kk]] = 1
            else:
                flavor[cm] = flavor[kk]
                weight[cm] = weight[kk]
                value[cm] = value[kk]
                cm = cm + 1
        l = cm

    return (phymac_num,result)
