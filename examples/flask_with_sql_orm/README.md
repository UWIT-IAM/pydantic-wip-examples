# Flask App with Sqlalchemy ORM Integration

This example demonstrates several features of pydantic:

- Translating from `snake_case` to `camelCase` for front/back-end naming consistency.
- `orm_mode`, which allows setting model fields by object fields
- JSON Schema exports (and how you can use it)
- A decent pattern for interfacing with ORMs

## Methodology

In general, it's considered bad practice to pass around your ORMs, as it leaves 
questions about the validity of the ORM instance 
(is it synced from the database? has it been manipulated by the service?). 
While there are a multitude of reasons to avoid the 
problem by simply not using ORMs, they can be useful for rapid prototyping of a new 
service when you're not so concerned with query efficiency. The good thing about 
this approach is that "business logic" is encapsulated, so when your product grows 
up and needs to ditch ORMs (🙌), you don't need to change your service logic, just 
your database access layer. 

Things that are good about this approach:

- Complete modularity and separation of concerns
- Avoids "chicken-and-egg" problems with record creation

Things that may be frustrating:

- Having to keep ORM definitions and pydantic models in sync (protecting yourself 
  against accidental changes also requires a lot of manual syncing of tests...)
- [Dependency cycles](https://github.com/samuelcolvin/pydantic/issues/659#issuecomment-797883881)
- Everyone hates ORMs, eventually


### A note about cyclical dependencies in ORM relationships

I didn't take the time to set up an example here, but the approach I have used in 
the past to avoid this issue is to allow pydantic models to only accept the foreign 
key field for a related model, and not the model itself. This allows referential 
lookups without recursing indefinitely. But, as you can imagine, this can result in 
a lot of queries being deferred, instead of selected one time. Therefore, point 3 
above applies: Everyone hates ORMs, eventually.

In other words, do **this**:

```

class Container(BaseModel):
    parent_id: Optional[int]
    child_ids: List[int] = []
```

and not **this**:

```
class Container(BaseModel):
    parent: Optional[Container]
    children: List[Container] = []
```