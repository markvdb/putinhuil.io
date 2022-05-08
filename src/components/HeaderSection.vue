<template>
  <header class="header-wrap">
    <div class="container">
      <div class="header">
        <span class="header-name">putinhuil.io</span>
        <a class="btn bg-blue" href="">donate</a>
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
  $yellow: #ffd100;
  .header-wrap {
    border-bottom: 2px solid $yellow;
    background: #fff;
    margin-bottom: 40px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 80px;

    &-name {
      font-size: 30px;
      font-weight: bold;
    }
  }
</style>
