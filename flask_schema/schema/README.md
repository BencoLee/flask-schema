# Jsonschema简明教程

[jsonschema官网地址](http://json-schema.org)

[jsonschema教程地址](https://spacetelescope.github.io/understanding-json-schema/index.html)

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
    "methods": {"type": "object"},
    "resource": {"type": "string"},
    "resources": {"type": "string"}
  }
}
```

简单解释一下，Object类型中关键字

- type：必须要有，用来解释这个json结构是属于什么类型
- properties：选填，如果这个是一个object类型，那么就需要对应的properties
- required：选填，用来确定properties中哪些元素是必须的

|         关键字          |             描述              |
| :------------------: | :-------------------------: |
|         type         |            定义类型             |
|      properties      |        定义属性，包括名字和类型         |
|       required       |            选择必选项            |
|    maxProperties     |           最大属性数量            |
|    minProperties     |           最小属性数量            |
| additionalProperties | True：允许有额外属性 False：不允许有额外属性 |

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

Valid: { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue" }
InValid: { "number": 1600, "street_name": "Pennsylvania", "street_type": "Avenue", "direction": "NW" }
```

