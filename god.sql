create table objects (
  objectID bigint not null primary key,
  title varchar(200),
  payload text,
  dataType varchar(200)
 
);


create table links (
  parentID bigint,
  childID bigint
);

