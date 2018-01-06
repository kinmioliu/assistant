from util import conf
from util import assistant_errcode
from util.conf import RESPONSIBILITY_FIELD_CONF
from base_assistant.models import ResponsibilityField

class ResponsibiltyFieldInfo:
    def __init__(self, groupname, introduce, plname):
        self.groupname = groupname
        self.introduce = introduce
        self.plname = plname

    def get_groupname(self):
        return self.groupname

    def get_introduce(self):
        return self.introduce

    def get_plname(self):
        return self.plname

    def set_attr(self, groupname, introduce, plname):
        self.groupname = groupname
        self.introduce = introduce
        self.plname = plname

    def __str__(self):
        return "groupname:" + self.groupname + "  introduce:" + self.introduce + "  plname:" + self.plname

    def to_model(self):
        responsefield_obj = ResponsibilityField.objects.filter(groupname__icontains=self.groupname)
        if len(responsefield_obj) == 0:
            return ResponsibilityField(groupname = self.groupname, introduce = self.introduce, plname = self.plname)
        else:
            return responsefield_obj[0]

class ResponsibiltyFieldParser:

    def parser_one_record(self, record, info):
        info.set_attr(record[0],record[1],record[2])
        return assistant_errcode.SUCCESS

    def update_or_create(self, info):
        defaults = {'introduce':info.get_introduce(),'plname':info.get_plname(),}
        try:
            obj = ResponsibilityField.objects.get(groupname=info.get_groupname())
            is_same = True
            for key, value in defaults.items():
                if (getattr(obj, key) != value):
                    is_same = False

            if not is_same:
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.save()
            else:
                return assistant_errcode.DB_SAME
            obj.save()
            return assistant_errcode.DB_UPDATED
        except ResponsibilityField.DoesNotExist:
            new_values = {'groupname': info.get_groupname()}
            new_values.update(defaults)
            obj = ResponsibilityField(**new_values)
            obj.save()
            return assistant_errcode.DB_CREATED

#     defaults = {}
# #        introduce = info.get_introduce(), plname = info.get_plname(),
#         obj, created = ResponsibilityField.objects.update_or_create(
#             groupname=info.get_groupname() ,
#             defaults = {'introduce':info.get_introduce(),'plname':info.get_plname(),}
#         )
#         conf.DUMP(obj)
#         conf.DUMP(created)
#         return created


    def run(self):
        result = dict()
        created_records = list()
        updated_records = list()
        for record in RESPONSIBILITY_FIELD_CONF:
            print(record)
            info = ResponsibiltyFieldInfo("", "", "")
            ret = self.parser_one_record(record, info)
            if ret != assistant_errcode.SUCCESS:
                continue

            ret = self.update_or_create(info)
            if ret == assistant_errcode.DB_SAME:
                conf.DUMP(info.__str__() + "SAME")
            elif ret == assistant_errcode.DB_UPDATED:
                updated_records.append(info.__str__())
                conf.DUMP(info.__str__() + "updated")
            elif ret == assistant_errcode.DB_CREATED:
                created_records.append(info.__str__())
                conf.DUMP(info.__str__() + "created")

        result['created'] = created_records
        result['updated'] = updated_records
        return result


