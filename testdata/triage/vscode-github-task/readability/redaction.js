const scrubFields=["password","secret_key","secretToken"];
module.exports=function scrub(event) {
  for (const field of scrubFields) delete event[field];
  return event;
};
