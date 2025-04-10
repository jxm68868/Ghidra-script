# export-Ghidra-Functions
该脚本的目的是：将ghidra中反编译的函数导出来。
![image](https://github.com/user-attachments/assets/3b4de05d-12f3-4988-8cf2-0814ff1e44c1)



这个ghidra脚本可以导出Ghidra中Symbol Tree下Functions的全部函数
脚本运行完毕后生成export_report.txt可以查看运行结果。

使用教程：
1.打开Ghidra-Windows-Script Manager
点击Create new script
![image](https://github.com/user-attachments/assets/0873c418-d941-4034-a484-38d8c8df2e4e)

2.创建脚本
选择python
![image](https://github.com/user-attachments/assets/c266f1e3-8465-496e-a6ea-af74c389ab8e)

![image](https://github.com/user-attachments/assets/3e4c71ca-18de-4583-807a-02228f2c9a32)
创建好脚本之后
把我的代码复制进去
![image](https://github.com/user-attachments/assets/711d3c1b-0250-425b-969c-066bd1c0ba32)

3.修改导出functions文件的路径
修改：base_dir = r"output_PATH"为自己想导出的目录路径

4.运行脚本即可
