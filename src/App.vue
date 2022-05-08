<template>
  <router-view/>
</template>

<style lang="scss">
  html, body, div, span, applet, object, iframe,
  h1, h2, h3, h4, h5, h6, p, blockquote, pre,
  a, abbr, acronym, address, big, cite, code,
  del, dfn, em, img, ins, kbd, q, s, samp,
  small, strike, strong, sub, sup, tt, var,
  b, u, i, center,
  dl, dt, dd, ol, ul, li,
  fieldset, form, label, legend,
  table, caption, tbody, tfoot, thead, tr, th, td,
  article, aside, canvas, details, embed, 
  figure, figcaption, footer, header, hgroup, 
  menu, nav, output, ruby, section, summary,
  time, mark, audio, video {
    margin: 0;
    padding: 0;
    border: 0;
    font-size: 100%;
    font: inherit;
    vertical-align: baseline;
  }
  /* HTML5 display-role reset for older browsers */
  article, aside, details, figcaption, figure, 
  footer, header, hgroup, menu, nav, section {
    display: block;
  }
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  } 
  body {
    background-color: #fbfbfb;
  }
  * {
    box-sizing: border-box;
  }
  button {
    box-shadow: none;
    border: 0;
    cursor: pointer;
  }
  .container {
    width: 100%;
    max-width: 1024px;
    margin: 0 auto;
    padding: 0 20px;
  }
  .section {
    margin: 0 0 40px;
  }
  .text {
    font-size: 16px;
    line-height: 1.45;
    margin-bottom: 20px;
  }
  $blue: #2b47ff;
  $yellow: #ffd100;
  .btn {
    padding: 10px 40px;
    text-decoration: none;
    font-weight: bold;
    font-size: 16px;
    border-radius: 20px;
    opacity: 1;
    transition: all 0.3s;
    display: inline-block;
    text-transform: uppercase;

    &:hover {
      opacity: 0.88;
    }
  }
  .bg-yellow {
    background: $yellow;
    color: #000;
  }
  .bg-blue {
    background: $blue;
    color: #fff;
  }
  .bg-black {
    background: #000;
    color: #fff;
  }
  .box {
    border: 2px solid $yellow;
    padding: 20px;
    background-color: #fff;
  }
  .center {
    text-align: center;
  }
</style>
