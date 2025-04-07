from tkzs_bd_db_tool.models import Base
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    Text,
    JSON,
    UniqueConstraint,
)


class TangLangLeadsTable(Base):
    __tablename__ = "tanglang_leads"
    __table_args__ = (
        UniqueConstraint("mts_lead_uuid", name="unique_mts_lead_uuid_mts_lead_id"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_0900_ai_ci",
            "mysql_row_format": "DYNAMIC",
            "schema": "jh_data",
        },
    )



    # 主键和基础信息
    key_id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    mts_lead_uuid = Column(String(36), comment="螳螂客户ID")
    mts_lead_id = Column(Integer, comment="螳螂客户id(后续弃用)")

    # 客户基本信息
    name = Column(String(50), comment="姓名")
    phone = Column(String(20), comment="手机号")
    phone2 = Column(String(20), comment="手机号2")
    qq = Column(String(20), comment="QQ")
    we_chat = Column(String(50), comment="微信")
    wechat2 = Column(String(50), comment="微信2")
    union_id = Column(String(50), comment="企业微信unionId")
    wechat_nick_name = Column(String(100), comment="企业微信昵称")

    # 教育相关信息
    first_course_name = Column(String(100), comment="一级项目名称")
    course_name = Column(String(100), comment="二级项目名称")
    course_id = Column(Integer, comment="二级项目ID")
    first_course_id = Column(Integer, comment="一级项目ID")
    education_name = Column(String(50), comment="学历")
    grade = Column(String(20), comment="年级")

    # 地域信息
    area_name = Column(String(50), comment="地域")
    province_area_name = Column(String(50), comment="地域-省份")
    residence = Column(String(100), comment="籍贯")
    adress = Column(String(200), comment="通讯地址")

    # 个人信息
    sex_code = Column(String(10), comment="性别")
    age = Column(Integer, comment="年龄")
    birthday = Column(String(10), comment="出生日期")
    nation = Column(String(20), comment="民族")
    document_type = Column(String(20), comment="证件类型")
    document_number = Column(String(50), comment="证件号码")

    # 联系信息
    email = Column(String(100), comment="邮箱")
    unit_name = Column(String(100), comment="工作单位")

    # 时间信息
    expected_time = Column(String(10), comment="预产期")
    create_time = Column(DateTime, comment="创建时间")
    update_time = Column(DateTime, comment="更新时间")
    first_touch_time = Column(DateTime, comment="首次跟单时间")
    last_touch_time = Column(DateTime, comment="最后一次跟单时间")
    first_assign_time = Column(DateTime, comment="首次分配时间")
    last_assign_time = Column(DateTime, comment="最后一次分配时间")
    last_call_time = Column(DateTime, comment="最后一次拨打日期")
    add_time = Column(DateTime, comment="添加时间")
    feedback_time = Column(DateTime, comment="最后一次反馈时间")
    next_visit_time = Column(DateTime, comment="下次跟单时间")

    # 来源跟踪
    source_mode = Column(String(50), comment="来源方式")
    source_type = Column(String(50), comment="推广来源类型名称")
    ad_name = Column(String(50), comment="广告商名称")
    visitor_id = Column(String(50), comment="访客id")
    chat_id = Column(String(50), comment="会话ID")
    url = Column(String(2048), comment="着陆页")
    prom_plan_name = Column(String(100), comment="计划名称")
    prom_unit_name = Column(String(100), comment="单元名称")
    prom_key_words = Column(String(100), comment="关键字")
    searchwd = Column(String(100), comment="搜索词")
    ip = Column(String(50), comment="ip")
    parea = Column(String(50), comment="Ip省份")
    carea = Column(String(50), comment="Ip城市")

    # 组织信息
    bu_id = Column(Integer, comment="事业部ID")
    bu_name = Column(String(50), comment="事业部名称")
    sea_bu_id = Column(Integer, comment="公海ID")
    sea_bu_name = Column(String(50), comment="公海名称")
    owner_org_id = Column(Integer, comment="呼叫组ID")
    owner_org_name = Column(String(50), comment="呼叫组名称")
    owner = Column(Integer, comment="归属人Id")
    owner_id = Column(String(50), comment="归属人")

    # 状态信息
    valid_flag_code = Column(String(20), comment="数据状态")
    intent = Column(String(20), comment="意向度")
    wechat_status = Column(String(20), comment="微信添加状态")
    qq_status = Column(String(20), comment="QQ添加状态")
    customer_status = Column(String(20), comment="客户状态")
    unconnect_reason = Column(String(100), comment="未接通原因")
    invalid_name = Column(String(50), comment="无效数据类型")
    is_add_enterprise_wechat = Column(String(10), comment="企业微信添加状态")

    # 其他信息
    tags = Column(String(500), comment="标签")
    content = Column(Text, comment="备注")
    custom_field_map = Column(JSON, comment="自定义字段")
    messages = Column(Text, comment="聊天内容")
    customer_type = Column(String(20), comment="名片类型")

    # 咨询师信息
    first_owner_name = Column(String(50), comment="首次咨询师")
    last_owner_name = Column(String(50), comment="最后咨询师")
    first_assign_owner_name = Column(String(50), comment="首次分配归属人")
    first_assign_org_name = Column(String(50), comment="首次分配归属机构")
    last_assign_type = Column(String(50), comment="最后一次分配类型")

    # 广告相关
    account_id = Column(Integer, comment="广告商账户ID")
    plan_id = Column(String(50), comment="广告商计划ID")
    unit_id = Column(String(50), comment="广告商单元ID")
    keyword_id = Column(String(50), comment="广告商创意ID")
    bcp_ssid = Column(String(50), comment="bcpID")

    # 报名信息
    sign_up_count = Column(Integer, comment="报名次数")
    account_name = Column(String(50), comment="账户名称")
    match_type = Column(String(50), comment="匹配方式")
    media = Column(String(50), comment="载体")
    submit_info_count = Column(String(20), comment="提交资料次数")
    submit_info_time = Column(String(50), comment="提交资料时间")

    # 微信扩展信息
    wechat_remark = Column(String(100), comment="微信备注")
    wechat_head_portrait = Column(String(500), comment="微信头像")

    # 操作人信息
    creater = Column(String(50), comment="创建人")
    updater = Column(String(50), comment="更新人")

    create_at = Column(DateTime, default=datetime.now, comment="数据库数据创建时间")
    update_at = Column(DateTime, onupdate=datetime.now, comment="数据库数据更新时间")


class TangLangReservationTable(Base):
    __tablename__ = "tanglang_reservations"
    __table_args__ = (
        UniqueConstraint("mst_resv_id", name="unique_mts_resv_id"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_0900_ai_ci",
            "mysql_row_format": "DYNAMIC",
            "schema": "jh_data",
        },
    )

    key_id = Column(Integer, primary_key=True,autoincrement=True,comment='主键ID')
    # 主键ID字段
    mstResvId = Column('mst_resv_id', Integer,  comment='螳螂预约单ID')
    mtsVisitId = Column('mts_visit_id', Integer, comment='螳螂咨询记录ID')
    mtsLeadUuid = Column('mts_lead_uuid', String(64), comment='螳螂客户ID')
    mtsLeadId = Column('mts_lead_id', Integer, comment='螳螂客户id(后续弃用)')
    
    # 基本信息字段
    orgName = Column('org_name', String(100), default="北京分校", comment='预约分校')
    content = Column('content', Text, comment='内容')
    resvTime = Column('resv_time', DateTime, comment='预约时间 yyyy-MM-dd HH:mm:ss')
    projectName = Column('project_name', String(100), comment='二级咨询项目')
    courseName = Column('course_name', String(100), comment='班型')
    
    # 状态和来源字段
    statusCode = Column('status_code', String(50), default="预约中", comment='预约单状态')
    sourceType = Column('source_type', String(50), default="在线", comment='来源方式')
    
    # 归属信息字段
    ownerName = Column('owner_name', String(100), comment='归属人')
    ownerOrg = Column('owner_org', String(100), comment='归属人机构')
    
    # 创建信息字段
    creater = Column('creater', String(100), comment='创建人')
    createrOrg = Column('creater_org', String(100), comment='创建人机构')
    createTime = Column('create_time', DateTime,comment='创建时间 yyyy-MM-dd HH:mm:ss')
    
    # 更新信息字段
    updater = Column('updater', String(100), comment='更新人')
    updateTime = Column('update_time', DateTime,comment='更新时间 yyyy-MM-dd HH:mm:ss')
    
    # 接待信息字段
    receptionName = Column('reception_name', String(100), comment='接待人')
    receptionOrg = Column('reception_org', String(100), comment='接待人机构')
    
    # 自定义字段
    reservatMap = Column('reservat_map', JSON, comment='自定义字段')
    
    create_at = Column(DateTime, default=datetime.now, comment="数据库数据创建时间")
    update_at = Column(DateTime, onupdate=datetime.now, comment="数据库数据更新时间")

    def __repr__(self):
        return f"<MantisReservation(id={self.mstResvId}, lead={self.mtsLeadUuid}, time={self.resvTime})>"
    