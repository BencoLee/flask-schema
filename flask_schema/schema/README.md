

# Jsonschema简明教程

[jsonschema官网地址](http://json-schema.org)

[jsonschema官方教程地址](https://spacetelescope.github.io/understanding-json-schema/index.html)

## Json schema格式

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "JsonSchema",
  "type": "object",
  "properties": {
    "id": {
      "description": "This is unique identifier",
      "type": "integer"
    },
    "name": {
      "description": "This is common name",
      "type": "string",
      "minLength": 4,
      "default": "zhihao",
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "exclusiveMinimum": true
    }
  },
  "required": ["id", "name", "age"]
}
```

|     关键字     |              描述              |
| :---------: | :--------------------------: |
|   $schema   | $schema关键字，表明这个模式符合v4规范，可以省略 |
|    title    |          标题，用来描述结构           |
| description |              描述              |
|    type     |             声明类型             |
| properties  |        定义属性，属性会在下面枚举         |
|  required   |            定义必须属性            |

## Json schema类型

### Object

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "title": "SchemaBase",
  "type": "object",
  "properties": {
    "name": {"not": [{"type": "array"}, {"type": "null"}]}
    "methods": {"type": "object"},
    "resource": {"type": "string"},
    "resources": {"type": "string"}
  },
  "required": ["methods", "resource", "resources"]
}
```

简单解释一下，Object类型中关键字

- type：必须要有，用来解释这个json结构是属于什么类型
- properties：选填，如果这个是一个object类型，那么就需要对应的properties
- required：选填，用来确定properties中哪些元素是必须的

|         关键字          |                    描述                    |
| :------------------: | :--------------------------------------: |
|         type         |                   定义类型                   |
|      properties      |               定义属性，包括名字和类型               |
|       required       |                  选择必选项                   |
|    maxProperties     |                  最大属性数量                  |
|    minProperties     |                  最小属性数量                  |
| additionalProperties | True：允许有额外属性 False：不允许有额外属性 Object：额外属性要满足这个对象要求 |
|  patternProperties   |        编写满足这个规则的属性，并且这个属性的类型是确定的         |
|     dependencies     |       某个属性被要求如果这个属性存在，必须它依赖的属性也要存在       |
|         not          |                 表示非这个类型                  |

**additionalProperties Example**

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": false
}
{
  "valid": { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" },
  "invalid": { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }
}
```

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": true
}
{
  "valid": { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }
}
```

```js
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
    "street_name": { "type": "string" },
    "street_type": { "type": "string",
                     "enum": ["Street", "Avenue", "Boulevard"]
                   }
  },
  "additionalProperties": {"type": "string"}
}
{
  "valid": { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }
  "invalid": { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "timestamp":  19930918}
}
```

**patternProperties Example**

```json
{
  "type": "object",
  "properties": {
    "number":      { "type": "number" },
  },
  "patternProperties": {
    "^S_": {"type": "string"},
    "^I_": {"type": "integer"}
  }
}
{
  "valid1": { "number": 42 },
  "valid2": { "S_42": "42"},
  "valid3": { "I_32": 32},
  "invalid1": {"S_42": 42},
  "invalid2": { "I_32": "32"},
}
```

**dependencies Example**

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "credit_card": { "type": "number" },
    "billing_address": { "type": "string" }
  },
  "required": ["name"],
  "dependencies": {
    "credit_card": ["billing_address"]
  }
}
{
  "valid1": {"name": "John Doe", "credit_card": 5555555555555555, "billing_address": "555 Debtor's Lane"},
  "valid2": {"name": "John Doe"},
  "valid3": {"name": "John Doe", "billing_address": "555 Debtor's Lane"},
  "invalid": {"name": "John Doe", "credit_card": 5555555555555555}
}
```



### Array

```json
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "methods": {
      "index": {
        "type": "object",
        "properties": {
          "products": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
            "uniqueItems": true
          }
        }
      }，
      "show": {
        "properties": {
          "students": {
            "type": "array",
      		"items": [
              {
                "type": "object",
      			"properties": {
                  "name": {"type": "string"}
      			}
              }
      		]
          },
			"minItems": 1,
			"maxItems": 60
        }
      }
    }
  },
  "required": ["methods", ]
}
```

array类型中有三个单独的属性：items，minItems，uniqueItems

|     关键字     |           描述           |
| :---------: | :--------------------: |
|    items    | 每个元素的类型，也可以用一个列表装着各种元素 |
|  minItems   |       数组中最少元素个数        |
|  maxItems   |       数组中最多元素个数        |
| uniqueItems |       约束每个元素都不相同       |

### String

```json
{
    "type": "object",
    "properties": {
        "ip": {
            "type": "string",
            "pattern":"w+([-+.]w+)*@w+([-.]w+)*.w+([-.]w+)*"
        },
        "host": {
            "type": "string",
            "pattern":"((d{3,4})|d{3,4}-)?d{7,8}(-d{3})*"
        },
    },
    "required": ["ip", "host"]
}
```

|    关键字    |    描述    |
| :-------: | :------: |
| maxLength | 最大长度>=0  |
| minLength | 最小长度>=0  |
|  pattern  | 用正则约束字符串 |

### Integer

Integer表示整形数值

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {
            "type": "integer",
          	"minimun": 0,
          	"exclusiveMinimum": true
        },
    },
    "required": ["name", "price"]
}
```

|       关键字        |        描述        |
| :--------------: | :--------------: |
|     minimum      |     约束最小值 >=     |
| exclusiveMinimum | 约束值要大于最小值才是有效值 > |
|     maximum      |     约束最大值 <=     |
| exclusiveMaximum | 约束值要小于最大值才是有效值 < |
|    multipleOf    |  是某数的整数倍，必须大于0   |

### Number

 number表示任意长度的浮点数值

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {
            "type": "number",
          	"minimun": 0,
          	"exclusiveMinimum": true
        },
    },
    "required": ["name", "price"]
}
```

|       关键字        |        描述        |
| :--------------: | :--------------: |
|     minimum      |     约束最小值 >=     |
| exclusiveMinimum | 约束值要大于最小值才是有效值 > |
|     maximum      |     约束最大值 <=     |
| exclusiveMaximum | 约束值要小于最大值才是有效值 < |

### Boolean

布尔类型，表示真或假

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "male": {"type": "boolean"},
    },
    "required": ["name", "male"]
}
```

### Enum

枚举类型，枚举默认值，可以有两种写法

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "projects": {
          "type": "string",
          "enum": ["math", "chinese", "english"]
        },
    },
    "required": ["name", "male"]
}
```

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "projects": ["math", "chinese", "english"]
    },
    "required": ["name", "projects"]
}
```

### Null

空类型

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "projects": {"type": "null"},
    },
    "required": ["name", "projects"]
}
```

### $ref & definitions

1. $ref，引用类型，可以用来引用其他schema
   - 支持http，https，file协议
   - 支持内部引用
2. definitions，当schema特别大的时候，可以创建内部结构体，再通过$ref引用

```json
{
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "projects": {"type": "null"},
        "warehouseLocation": {"$ref": "http://json-schema.org/geo"}
    },
    "required": ["name", "projects", "warehouseLocation"]
}
```

```json
{
    "type": "array",
    "items": { "$ref": "#/definitions/positiveInteger" },
    "definitions": {
        "positiveInteger": {
            "type": "integer",
            "minimum": 0,
            "exclusiveMinimum": true
        }
    }
}
```

### allOf

意思是约束需要所有元素，不建议使用，可以使用required替代

```json
{
  "definitions": {
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" }
      },
      "required": ["address", "city", "state"]
    }
  },

  "allOf": [
    { "$ref": "#/definitions/address" },
    { "properties": {
        "type": { "enum": [ "residential", "business" ] }
      }
    }
  ]
}
```

### anyOf

意思是约束需要任意元素

```json
{
  "anyOf": [
    {"type": "string"}，
    {"type": "number"}
  ]
}
```

### oneOf

意思是约束选择其中一个元素

```json
{
  "oneOf": [
    {"type": "string"}，
    {"type": "number"}
  ]
}
```

