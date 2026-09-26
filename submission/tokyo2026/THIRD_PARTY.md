# Third-party materials

New project source is MIT. No third-party source is vendored.

| Tool / reference | Version / pin | License / use |
|---|---|---|
| Python | Tested 3.14.7; CI 3.12 | PSF; standard-library runtime |
| Foundry Anvil/Cast | 1.8.3, cae51ad458f6abb64852b7709eb784352429825d | MIT OR Apache-2.0; external execution/ABI tools |
| Node.js | Tested 20.18.0; CI 22 | Node.js license; validator tests |
| Playwright CLI | 0.1.21 | Apache-2.0; external browser testing/recording |
| FFmpeg | 9.0.1 installed build | Installed build GPL components; media tooling, not distributed |
| Uniswap ISwapRouter | 764903fe5c8e274dc107163347cc2404ca0fd584 | GPL-2.0-or-later interface reference; not vendored |
| GitHub Actions | SHA-pinned in workflows | Respective official action licenses; CI and Pages |

The deployed Uniswap protocol and token contracts are accessed through their public ABI on a local
fork; this repository does not deploy, relicense or distribute the protocol contract source.
Browser rendering uses system fonts and newly authored CSS. No pre-event Entrotter assets are included.
