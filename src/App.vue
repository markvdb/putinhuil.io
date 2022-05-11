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
  input {
    border:none;
    background-image:none;
    background-color:transparent;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;
  }
  $blue: #2b47ff;
  $yellow: #ffd100;
  $grey: #f5f7f9;

    body {
      font-family: Avenir, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
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
    padding: 50px 0;
    background: #FFF;
    &.bg {
      background-color: $grey;
    }
  }
  .title {
    font-size: 20px;
    letter-spacing: 0.2px;
    text-transform: uppercase;
    margin-bottom: 40px;
  }
  .text {
    font-size: 16px;
    line-height: 1.45;
    margin-bottom: 20px;
    letter-spacing: 0.2px;
  }
  
  .btn {
    padding: 10px 30px;
    text-decoration: none;
    font-weight: bold;
    font-size: 16px;
    border-radius: 3px;
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
    padding: 20px;
    background-color: #fff;
      &.border {
        border-radius: 3px;
        box-shadow: 0 1px 4px 0 rgba(138,138,138,0.3);
      }
      &.transparent {
        background-color: transparent;
        padding: 0 20px;
      }
  }
  .center {
    text-align: center;
  }
</style>
