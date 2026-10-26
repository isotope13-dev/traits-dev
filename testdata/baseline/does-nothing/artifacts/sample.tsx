import React from "react";

interface SampleProps {
  message: string;
}

export default function Sample({ message }: SampleProps): JSX.Element {
  return (
    <section className="sample">
      <p>{message}</p>
    </section>
  );
}
