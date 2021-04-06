create database if not exists interface_autotest default charset utf8 collate utf8_general_ci;

create table interface_api(
	api_id int not null auto_increment comment "自增长主键",
	api_name varchar(50) not null comment "接口名称",
	r_url varchar(50) not null comment "请求接口的URL",
    r_method varchar(10) not null comment "接口请求方式",
    p_type varchar(20) not null comment "传参方式",
    status tinyint default 0,
    ctime datetime,
    unique index(api_name),
    primary key(api_id)
)engine=InnoDB default charset=utf8;

create table interface_test_case(
    id int not null AUTO_INCREMENT comment "自增长主键",
    api_id int not null comment "对应interface_api的api_id",
    r_data varchar(255) comment "请求接口时传的参数",
    rely_data varchar(255) comment "用例依赖的数据",
    protocol_code int comment "接口期望响应code",
    res_data varchar(255) comment "接口响应body",
    data_store varchar(255) comment "依赖数据存储",
    check_point varchar(255) comment "接口响应校验依据数据",
    status tinyint default 0 comment "用例执行状态，0不执行，1执行",
    error_info varchar(1000) comment "错误信息列",
    ctime datetime,
    primary key(id),
    index(api_id)
)engine=InnoDB default charset=utf8;

create table interface_data_store(
    api_id int not null comment "对应interface_api的api_id",
    case_id int not null comment "对应interface_test_case里面的id",
    data_store varchar(255) comment "存储的依赖数据",
    ctime datetime,
    index(api_id,case_id)
)engine=InnoDB default charset=utf8;


alter table interface_data_store add id int not null AUTO_INCREMENT primary key before api_id;










