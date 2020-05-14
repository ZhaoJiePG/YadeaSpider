# Author:Aliex ZJ
# !/usr/bin/env python3
# -*- coding:utf-8 -*-
end_index = 3
append_str1 = ''
append_str2 = ''
append_str3 = ''
append_str4 = ''
append_str5 = ''
append_str6 = ''
append_str7 = ''
append_str8 = ''
append_str9 = ''
append_str10 = ''
append_str11 = ''
append_str12 = ''
append_str13 = ''
append_str14 = ''
sql2 = ''
column_list1 = []

for index in range(1, end_index + 1):

    column = 'weike' + str(index)
    last_column = 'weike' + str(index - 1)
    after_column = 'weike' + str(index + 1)
    column_direct = column + '_direct'
    column_sum_rownumber1 = 'sum(if({0} is not null and {1}_rownumber=1,1,0)) over(partition by {2}) as {3}_direct'.format(
        column, column, after_column, column)

    # append_str1-3
    append_str1 = column
    append_str2 = append_str2 + '\n,{0}.wid as {1}'.format(column, column)
    append_str3 = append_str3 + '''
                left join ods.s07_spider_weimeng_merchant_weike_list as {0}
                on {1}.inviter={2}.wid
                '''.format(column, column, last_column)
    # append_str4
    if (index == end_index):
        append_str4 = append_str4 + column
    else:
        append_str4 = append_str4 + column + ',\n' + column_direct + ',\n'

    # append_str5
    if (index == end_index):
        append_str5 = append_str5 + column
    else:
        append_str5 = append_str5 + column + ',' + column_sum_rownumber1 + ',\n'

    # column_list1
    append_str6 = append_str6 + after_column + ','
    column_list1.append(append_str6[:-1])

    # append_str7
    if (index == 1):
        append_str7 = ''
    else:
        append_str7 = append_str7 + 'row_number() over(partition by {0}) {1}_rownumber,{2},'.format(
            column_list1[index - 2], last_column, column)

    for i in range(index, end_index + 1):
        append_str8 = append_str8 + '''select 
           '{0}' as desc,
            {1} as root_node,
            {2} as master_node,
            {3} as slave_node,
            {4}_direct as direct_num
        from 
            dw.dw_weimeng_weike_invite_relation_temp
        group by 
            1,2,3,4,5'''.format(column, column, 'weike' + str(i - 1), 'weike' + str(i), 'weike' + str(i)) + '\n union \n'

print(append_str8)

print(sql2)
