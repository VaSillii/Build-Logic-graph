import re
from pathlib import Path

from HelperClass.logic_operation import EquivalentClass, Intersection, Node, Negation, \
    UniversalRestriction, ExistentionRestriction, Union, SubclassOf
from HelperClass.operationClass import OperationClass


class ParseOntology(object):
    def __init__(self, path_file: Path):
        self.class_onto = []
        self.path = path_file
        self.name_onto = ParseOntology.get_name_onto(self.path)

    @staticmethod
    def get_name_onto(path):
        path_str = str(path).replace('/', '\\')
        path_list = path_str.split('\\')
        return path_list[-1].split('.owl')[0]

    def check_exist_class(self, operation: OperationClass) -> bool:
        """
        Check exist class in list by name
        :param operation: Object OperationClass
        :return: Bool
        """
        return operation in self.class_onto

    @staticmethod
    def _get_name_element_from_url(class_name_url: str) -> str:
        """
        Get name class from url
        :param class_name_url: Url class
        :return: Class name without url
        """
        if class_name_url.find('#') != -1:
            return class_name_url[class_name_url.find('#') + 1:]
        return class_name_url

    @staticmethod
    def _get_attribute_info(name_attr: str, operation: str) -> str:
        """
        Get attribute data from operation
        :param name_attr: Attribute name
        :param operation: Operation
        :return: Data attribute
        """
        about = re.search(f':{name_attr}=\"[\w:\-\/\.#]+\"', operation)
        if about:
            about = re.findall("\"(.*?)\"", about.group(0))[0]
        return about

    @staticmethod
    def get_operation(operation):
        op = re.search(r':[A-Za-z0-9_]+', operation)
        if op:
            return op.group()[1:]
        return None

    @staticmethod
    def _parse_restriction(op_list):
        first_op = ParseOntology.get_operation(op_list[0])
        first_res = ParseOntology._get_name_element_from_url(ParseOntology._get_attribute_info('resource', op_list[0]))
        second_op = ParseOntology.get_operation(op_list[1])
        some_element = op_list[1:]
        if second_op == 'someValuesFrom':
            universal_restriction = UniversalRestriction()
            universal_restriction.first_el.append(Node(name=''))
            if len(some_element) == 1 and some_element[0][-2] == '/':
                second_res = ParseOntology._get_name_element_from_url(ParseOntology._get_attribute_info('resource', op_list[1]))
                universal_restriction.arrow_name = first_res
                universal_restriction.second_el.append(Node(name=second_res))
                return universal_restriction
            universal_restriction.second_el.append(ParseOntology.parse_nested_op(some_element[1:-1]))

            return universal_restriction
        elif second_op == 'allValuesFrom':
            existention_restriction = ExistentionRestriction()
            existention_restriction.first_el.append(Node(name='', flag_negation=True))
            existention_restriction.arrow_name = first_res
            if len(some_element) == 1 and some_element[0][-2] == '/':
                second_res = ParseOntology._get_name_element_from_url(
                    ParseOntology._get_attribute_info('resource', op_list[1]))
                existention_restriction.second_el.append(Node(name=second_res, flag_negation=True))
                return existention_restriction
            elm = ParseOntology.parse_nested_op(some_element[1:-1])
            if len(elm) == 1:
                existention_restriction.second_el.append(elm[0])
            else:
                existention_restriction.second_el += elm

            return existention_restriction
        return None

    @staticmethod
    def _parse_complement_of(op_list):
        negation = Negation()
        if len(op_list) == 1:
            class_name = ParseOntology._get_name_element_from_url(
                ParseOntology._get_attribute_info('resource', op_list[0]))
            negation.elements.append(Node(name=class_name))
            return negation
        negation.elements = ParseOntology.parse_nested_op(op_list)

        return negation

    @staticmethod
    def parse_nested_op(operations_list):
        result = []
        flag_read = False
        open_flag_cnt = 0
        flag_reset = False
        op_list = []

        for op in operations_list:
            if flag_reset:
                flag_read = False
                open_flag_cnt = 0
                flag_reset = False
                op_list = []

            if re.search(r'<[A-Za-z0-9-_/]+:equivalentClass.*>', op) or re.search(r'<[A-Za-z0-9-_/]+:Class.*>', op):
                continue

            if re.search(r'<[A-Za-z0-9-_/]+:Description.*>', op):
                if not flag_read:
                    class_name = ParseOntology._get_name_element_from_url(
                        ParseOntology._get_attribute_info('about', op))
                    result.append(Node(name=class_name))
                    flag_reset = True
                    continue
                else:
                    op_list.append(op)
                    continue

            if re.search(r'<[A-Za-z0-9-_]+:intersectionOf', op):
                if not flag_read:
                    flag_read = True
                op_list.append(op)
                open_flag_cnt += 1
                continue

            if re.search(r'<[A-Za-z0-9-_]+:unionOf', op):
                if not flag_read:
                    flag_read = True
                op_list.append(op)
                open_flag_cnt += 1
                continue

            if re.search(r'<[A-Za-z0-9-_]+:Restriction', op):
                if not flag_read:
                    flag_read = True
                op_list.append(op)
                open_flag_cnt += 1
                continue

            if re.search(r'<[A-Za-z0-9-_]+:complementOf.*>', op):
                if op[-2] == '/':
                    if not flag_read:
                        op_list.append(op)
                        result.append(ParseOntology._parse_complement_of(op_list))
                        flag_reset = True
                        continue
                    else:
                        op_list.append(op)
                        continue
                if not flag_read:
                    flag_read = True
                op_list.append(op)
                open_flag_cnt += 1
                continue

            if re.search(r'<[A-Za-z0-9-_]+:someValuesFrom.*>', op):
                if op[-2] == '/':
                    if not flag_read:
                        op_list.append(op)
                        result.append(ParseOntology._parse_complement_of(op_list))
                        flag_reset = True
                        continue
                    else:
                        op_list.append(op)
                        continue
                if not flag_read:
                    flag_read = True
                op_list.append(op)
                open_flag_cnt += 1
                continue

            if flag_read:
                op_list.append(op)
                if re.search(r'</[A-Za-z0-9-_]+:intersectionOf', op):
                    open_flag_cnt -= 1
                    if open_flag_cnt == 0:
                        operation = ParseOntology._parse_intersection(op_list[1:-1])
                        result.append(operation)
                        flag_reset = True
                        continue
                if re.search(r'</[A-Za-z0-9-_]+:unionOf', op):
                    open_flag_cnt -= 1
                    if open_flag_cnt == 0:
                        op = ParseOntology._parse_union_of(op_list[1:-1])
                        result.append(op)
                        flag_reset = True
                        continue
                if re.search(r'</[A-Za-z0-9-_]+:Restriction', op):
                    open_flag_cnt -= 1
                    if open_flag_cnt == 0:
                        operation = ParseOntology._parse_restriction(op_list[1:-1])
                        result.append(operation)
                        flag_reset = True
                        continue
                if re.search(r'</[A-Za-z0-9-_]+:complementOf', op):
                    open_flag_cnt -= 1
                    if open_flag_cnt == 0:
                        op = ParseOntology._parse_complement_of(op_list[1:-1])
                        flag_reset = True
                        result.append(op)
                        continue
                continue
        return result

    @staticmethod
    def _parse_intersection(op_list):
        inter = Intersection()
        inter.elements = ParseOntology.parse_nested_op(op_list)
        return inter

    @staticmethod
    def _parse_union_of(op_list):
        union = Union()
        union.elements = ParseOntology.parse_nested_op(op_list)
        return union

    @staticmethod
    def _handle_sub_class_of(sub_class_of: list):
        if len(sub_class_of) < 2:
            return None
        sub = SubclassOf()
        sub.elements = ParseOntology.parse_nested_op(sub_class_of[1:-1])
        return sub

    @staticmethod
    def _handle_equivalent(equivalent_class: list):
        eq_class = EquivalentClass()

        if len(equivalent_class) == 1:
            class_name = ParseOntology._get_name_element_from_url(
                ParseOntology._get_attribute_info('resource', equivalent_class[0]))
            eq_class.name = class_name
            return eq_class

        eq_class.elements = ParseOntology.parse_nested_op(equivalent_class)
        return eq_class

    def _handle_operation(self, operation_list: list):
        """
        Handle list operation
        :param operation_list: Operation list
        """
        if not operation_list:
            return None

        class_name = ParseOntology._get_name_element_from_url(
            ParseOntology._get_attribute_info('about', operation_list[0]))
        if class_name is None:
            return None
        op = OperationClass(name=class_name)


        if len(operation_list) != 1:
            equivalent_class = []
            flag_reset = False
            flag_add_element = False
            for operation in operation_list:
                if flag_reset:
                    equivalent_class = []
                    flag_reset = False
                    flag_add_element = False

                if re.search(r'<[A-Za-z0-9-_]+:equivalentClass.*>', operation):
                    flag_add_element = True
                    if len(operation) > 2 and operation[-2] == '/':
                        equivalent_class.append(operation)
                        eq = self._handle_equivalent(equivalent_class)
                        op.equivalent_class.append(eq)
                        flag_reset = True
                        continue
                if re.search(r'<[A-Za-z0-9-_]+:subClassOf.*>', operation):
                    flag_add_element = True
                    if len(operation) > 2 and operation[-2] == '/':
                        sub_class = ParseOntology._get_name_element_from_url(
                            ParseOntology._get_attribute_info('resource', operation))
                        sub_el = SubclassOf()
                        sub_el.elements.append(Node(name=sub_class))
                        op.sub_class_of.append(sub_el)
                        flag_reset = True
                        continue

                if flag_add_element:
                    equivalent_class.append(operation)

                if re.search(r'</[A-Za-z0-9-_]+:equivalentClass.*>', operation):
                    eq = ParseOntology._handle_equivalent(equivalent_class)
                    op.equivalent_class.append(eq)
                    flag_reset = True
                    break
                    continue

                if re.search(r'</[A-Za-z0-9-_]+:subClassOf.*>', operation):
                    sub_el = ParseOntology._handle_sub_class_of(equivalent_class)
                    op.sub_class_of.append(sub_el)
                    flag_reset = True
                    continue

        if not self.check_exist_class(op):
            self.class_onto.append(op)

    def parse(self):
        self.get_data()

    def get_data(self):
        """
        Get description ontology in json
        :return: Json description ontology
        """
        list_onto_class = []
        with open(self.path, 'r', encoding='utf-8') as f:
            operation_list = []
            flag_read = False
            flag_reset = False
            open_flag_cnt = 0

            while True:
                line = f.readline()
                if not line:
                    break

                if flag_reset:
                    operation_list = []
                    flag_read = False
                    flag_reset = False
                    open_flag_cnt = 0

                line_format = ' '.join(line.split())

                if len(line_format) == 0:
                    flag_reset = True
                    continue

                if flag_read:
                    operation_list.append(line_format)
                    if re.search('<[A-Za-z0-9-_]+:Class*>', line_format) is not None:
                        open_flag_cnt += 1

                    if re.search(r'<\/[A-Za-z0-9-_]+:Class>', line_format) is not None:
                        open_flag_cnt -= 1
                        if open_flag_cnt == 0:
                            flag_reset = True
                            self._handle_operation(operation_list)
                            # break
                            continue
                    continue

                if re.search('<[A-Za-z0-9-_]+:Class.*>', line_format) is not None:
                    # Line operation
                    operation_list.append(line_format)
                    open_flag_cnt += 1
                    if line_format[-2:] == '/>':
                        self._handle_operation(operation_list)
                        flag_reset = True
                    # Nested operation
                    flag_read = True
                    continue


if __name__ == '__main__':
    path = Path(__file__).absolute().parent.joinpath(r'File\test_onto.owl')
    path = Path(__file__).absolute().parent.joinpath(r'File\family.owl')
    parse_onto = ParseOntology(path)
    data = parse_onto.get_data()
    # print(data.class_onto[0].equivalent_class[0].elements[0].name)
