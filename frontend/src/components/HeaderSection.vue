<template>
  <header class="header-wrap">
    <div class="container full">
      <div class="header">
        <span class="header-name">putinhuil.io</span>
        <div id="menuBtn" class="header-menu" @click="sideMenu($event)" v-bind:class="{ active: menu }">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>
    <nav ref="menu" @focusout="sideMenu($event)" tabindex="-1" class="nav-bar"  id="menuBar" v-bind:class="{ active: menu }">
      <p class="nav-msg text">
        Some info text<br>
        Some info text
      </p>
      <ul class="nav-list">
        <li class="nav-list-item">
          <a target="_blank" href="" class="nav-link">link1</a>
        </li>
        <li class="nav-list-item">
          <a target="_blank" href="" class="nav-link">link2</a>
        </li>
        <li class="nav-list-item">
          <a target="_blank" href="" class="nav-link">link3</a>
        </li>
        <li class="nav-list-item">
          <a target="_blank" href="" class="nav-link">Our facebook</a>
        </li>
        <li class="nav-list-item">
          <a target="_blank" href="" class="nav-link">Our twitter</a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'HeaderSection',
  data() {
    return {
      menu: false,
      shown: false
    }
  },
  methods: {
    sideMenu(event) {
      let clicked = event.target;
      if (!this.menu && !this.shown) {
        const elem = this.$refs.menu;
        setTimeout(() => {
          elem.focus();
          this.shown = true;
        }, 1);
        this.menu = true; //show menu
      } else {
        if (!clicked.contains(event.relatedTarget)) { //check if not child node
          this.menu = false; //hide menu
          setTimeout(() => {
            this.shown = false; //avoid conflcit button click and focusout menu
          }, 200);
        }
      }
    },
  }
}
</script>

<style scoped lang="scss">
  $blue: #66b0ff;
  $yellow: #ffd100;
  .header-wrap {
    border-bottom: 2px solid $yellow;
    background: #fff;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 40px;

    &-name {
      font-size: 16px;
      font-weight: bold;
    }

    &-menu {
      background: $yellow;
      border-radius: 3px;
      width: 30px;
      height: 30px;
      padding: 5px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      cursor: pointer;
      opacity: 1;
      transition: all 0.3s;

      position: absolute;
      top: 5px;
      right: 20px;
      z-index: 10;

      &:hover {
        opacity: 0.88;
      }

      span {
        height: 2px;
        background: #fff;
        display: block;
        width: 100%;
        border-radius: 3px;
        transition: .2s;
        transform-origin: center center;
        margin: 2px 0px;
        position: relative;
      }

      &.active {
        position: fixed;
        span {
          margin: 0;
        }
        span:nth-child(1) {
          transform: rotate(45deg);
          top: 2px;
        }
        span:nth-child(2) {
          transform: translateX(20px);
          opacity: 0;
        }
        span:nth-child(3) {
          top: -2px;
          transform: rotate(-45deg);
        }
      }
    }
  }

  .nav {
    &-bar {
      position: fixed;
      top: 0;
      right: 0;
      width: 300px;
      height: 100vh;
      padding: 60px 30px;
      background-color: #fff;
      box-shadow: 0 1px 4px 0 rgba(138, 138, 138, 0.3);
      z-index: 9;
      transform: translateX(100%);
      transition: 0.5s ease all;
      outline: none !important;
      &.active {
        transform: translateX(0%);
      }
    }

    &-list {
      list-style: none;

      &-item {
        margin: 5px 0;
        border-bottom: 1px solid #dfdfdf;

        &:first-child {
          margin-top: 0;
        }
        &:last-child {
          margin-bottom: 0;
          border-bottom: 0;
        }
      }
    }

    &-link {
      text-decoration: none;
      color: $blue;
      padding: 8px 0;
      display: inline-block;
      font-size: 16px;
      letter-spacing: 0.2px;
    }
    
  }
</style>
