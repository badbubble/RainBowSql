# RainBowSql

-----

山东科技大学
数据库 课程设计

* [x] 有用户名和密码 0.5
* [x] 有权限管理 0.5
* [x] 解析CREATE、SELECT、INSERT、DELETE、UPDATE等SQL语句的内容；检查SQL语句中的语法错误和语义错误；5 x 0.2 = 2.5
* [ ] 输入“help(show) database”命令，输出所有数据表、视图和索引的信息，同时显示其对象类型；0.25
* [x] 输入“help(show) table 表名”命令，输出数据表中所有属性的详细信息 0.25
* [ ] 输入“help(show) view 视图名”命令，输出视图的定义语句；0.25
* [ ] 输入“help(show) index 索引名”命令，输出索引的详细信息 0.25
* [ ] 执行SELECT语句，从自主设计的数据表中查询数据，并输出结果；在SELECT语句中需要支持GROUP BY、HAVING和ORDER BY子句，需要支持5种聚集函数,单表查询占0.4分、连接查询占0.4分 2 x 0.4 = 0.8
* [ ]执行CREATE语句，创建数据表、视图、索引三种数据库对象；创建数据表时需要包含主码、外码、唯一性约束、非空约束等完整性约束的定义；{创建数据表0.5分，视图0.3分，索引0.2分；对于create table，要支持主码、外码、unique、null和not null、check约束，约束缺失扣除0.2分} 0.5 + 0.3 + 0.2 = 1.0
* [ ] 执行INSERT、DELETE和UPDATE语句，更新数据表的内容；更新过程中需要检查更新后的数据表是否会违反参照完整性约束。如果是，则提示违反哪一条完整性约束，并拒绝执行更新操作；如果否，提示数据表更新成功，并说明插入、删除或修改了几个元组。{insert语句占0.4分，update语句占0.4分，delete语句占0.2分，insert要实现单个元组的插入和元组集合的插入（带子查询），要检查实体完整性（唯一和非空），参照完整性约束和check约束，约束缺失扣除0.2分。 delete和update要支持where子句（and、or、between and、in、like），条件缺失和约束检查缺失扣除0.2分}  1.0
* [ ] 执行GRANT语句，为用户授予对某数据库对象的SELECT、INSERT、DELETE、UPDATE等权限；执行REVOKE语句，收回上述权限；{grant和revoke各占0.5分} 1.0