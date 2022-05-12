<template>
  <header class="header-wrap">
    <div class="container">
      <div class="header">
        <span class="header-name">putinhuil.io</span>
        <!-- <a class="btn bg-blue" href="">donate</a> -->
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'HeaderSection'
}
</script>

<style scoped lang="scss">
  $blue: #2b47ff;
  $yellow: #ffd100;
  .header-wrap {
    border-bottom: 2px solid $yellow;
    background: #fff;
  }
  .header {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 30px;

    &-name {
      font-size: 16px;
      font-weight: bold;
    }
  }
</style>
