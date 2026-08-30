# OOP Assessment Reference

## OOP Foundations
An object has identity, state, and behavior; a class defines a family of objects. OOP quality comes from responsibility boundaries, not from turning every value into a class.
## Classes & Objects
Instance members belong to each object, while static members belong to the class. Cohesion means a class has a focused purpose; constructors should establish valid state.
## Encapsulation
Encapsulation protects invariants through controlled access, not merely private fields with unrestricted setters. Good answers explain information hiding and behavior-oriented APIs.
## Abstraction & Interfaces
Abstraction exposes essential contracts while hiding implementation details. Interfaces reduce coupling when clients depend on capabilities instead of concrete types.
## Inheritance
Inheritance is appropriate for substitutable is-a relationships. Reuse alone is insufficient justification, and deep hierarchies often create fragile coupling.
## Polymorphism
Subtype polymorphism lets one interface dispatch to different implementations at runtime. Overloading is compile-time selection and is not runtime polymorphism.
## Composition
Composition builds behavior from owned collaborators and delegation. It usually changes more safely than inheritance and models has-a rather than is-a relationships.
## Object Construction
Constructors, factories, and builders create valid objects under different complexity needs. Immutability requires preventing observable state changes, not only declaring a reference final.
## Method Overloading & Overriding
Overloads share a name but differ in parameters; overrides replace inherited behavior with a compatible signature. Return types alone cannot distinguish overloads in common languages.
## SOLID Principles
SRP concerns reasons to change; OCP supports extension without repeated modification; LSP preserves substitutability; ISP favors focused contracts; DIP points dependencies toward abstractions.
## Design Patterns
Patterns are named trade-off-bearing solutions, not mandatory templates. Assess when Strategy, Factory, Observer, Adapter, Decorator, or similar patterns reduce real coupling.
## Exception Handling
Exceptions should preserve context and be handled where recovery or translation is meaningful. Catching everything, swallowing failures, or using exceptions for normal control flow are warning signs.
## Generics & Collections
Generics provide reusable type safety, while collection choice depends on order, uniqueness, access, mutation, and complexity. Variance controls safe subtype relationships between generic types.
## Equality & Object Contracts
Equal objects must produce equal hash codes, and equality should be reflexive, symmetric, transitive, consistent, and null-safe. Mutable hash keys can break hash collections.
## Object-Oriented Design
Good designs assign responsibilities, minimize coupling, maximize cohesion, and isolate change. Evaluate requirements, collaborators, boundaries, testability, and explicit trade-offs.
