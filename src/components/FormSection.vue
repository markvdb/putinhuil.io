<template>
  <section class="section">
    <div class="container">
      <div class="box">
        <p class="text form-title">
          When I take a European flight, how many euros end up in the pockets of Putin and his cronies? 
          <br>
          Putinhuil.io tries to answer that question for you. 
        </p>
        <div class="calculate-form">
          <div class="form-group">
            <label for="" class="form-label">Airport A</label>
            <simple-typeahead
              id="airportA"
              class="form-input"
              placeholder="Start writing..."
              :items="items"
              :minInputLength="1"
              :itemProjection="itemProjectionFunction"
              @selectItem="selectItemEventHandler"
              @onInput="onInputEventHandler"
              @onFocus="onFocusEventHandler"
              @onBlur="onBlurEventHandler"
            >
          </simple-typeahead>
          </div>
          <div class="form-group">
            <label for="" class="form-label">Airport B</label>
            <simple-typeahead
              id="airportB"
              class="form-input"
              placeholder="Start writing..."
              :items="items"
              :minInputLength="1"
              :itemProjection="itemProjectionFunction"
              @selectItem="selectItemEventHandler"
              @onInput="onInputEventHandler"
              @onFocus="onFocusEventHandler"
              @onBlur="onBlurEventHandler"
            >
          </simple-typeahead>
          </div>
          <button @click="calculate" class="btn bg-black form-button">calculate</button>
        </div>
        <div class="calculate-switch">
          <div class="calculate-radio">
            <div class="radio-group">
              <input class="calculate-radio-input" checked type="radio" id="one" value="one" v-model="way" />
              <label class="calculate-radio-label" for="one">One way</label>
            </div>
            <div class="radio-group">
              <input class="calculate-radio-input" type="radio" id="two" value="two" v-model="way" />
              <label class="calculate-radio-label" for="two">With return</label>
            </div>
          </div>
          <div class="calculate-result">
            Earned:
            <span class="calculate-result-value" v-if="way == 'one'">{{ resultOne }}$</span>
            <span class="calculate-result-value" v-else>{{ resultTwo }}$</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import SimpleTypeahead from 'vue3-simple-typeahead'
// import 'vue3-simple-typeahead/dist/vue3-simple-typeahead.css' //Optional default CSS

export default {
  name: 'FormSection',
  components: {
    SimpleTypeahead
  },
  data() {
    return {
      way: 'one',
      resultOne: 1.00,
      resultTwo: 2.00,
      items: ['One','Two','Three']
    }
  },
  methods: {
    calculate() {
      //change sum for both options (one/two ways)
      console.log('calculate sum');
      // this.resultOne = x;
      // this.resultTwo = x;
    }
  }
}
</script>

<style lang="scss">
  $form-max: 100%;
  .calculate-form {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20px;
    max-width: $form-max;
  }
  .form {
    &-group {
      margin-right: 20px;
      flex: 1;
    }
    &-label {
      display: block;
      font-size: 13px;
      font-weight: bold;
      margin-bottom: 5px;
    }
    &-input {
      .simple-typeahead-input {
        max-width: 330px;
        width: 100%;
        padding: 8px 5px;
        font-size: 16px;
      }
    }
    &-button {
      margin: auto 0 0 auto;
    }
  }
  .calculate-switch {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: $form-max;
    flex-wrap: wrap;
  }
  .calculate-result {
    display: flex;
    align-items: flex-end;
    font-size: 24px;
    font-weight: bold;
    &-value {
      color: #e00505;
      font-size: 34px;
      padding-left: 10px;
      line-height: 1;
    }
  }
  .calculate-radio {
    &-input {
      margin-left: 0;
      margin-right: 5px;
    }
    &-label {
      font-size: 16px;
      line-height: 1.45;
    }
  }
  .radio-group {
    &:first-child {
      margin-bottom: 10px;
    }
  }
  .simple-typeahead {
    position: relative;
    width: 100%;
    font-size: 16px;

    &-list {
      position: absolute;
      width: 100%;
      border: none;
      max-height: 400px;
      overflow-y: auto;
      z-index: 10;
      border-bottom: 1px solid #d1d1d1;

      
      &-item {
        font-size: 14px;
        background-color: #fff;
        padding: 3px 8px;
        border-bottom: 1px solid #d1d1d1;
        border-left: 1px solid #d1d1d1;
        border-right: 1px solid #d1d1d1;
        cursor: pointer;
        &:last-child {
          border-bottom: 0;
        }
        &:hover,
        &.active {
          background-color: #f1f1f1;
        }
      }
    }
  }
  
  @media screen and (max-width: 768px) {
    .calculate-form {
      flex-direction: column;
      align-content: center;
    }
    .form-group {
      margin: 0 0 20px 0;
      width: 100%;
    }
    .form-input .simple-typeahead-input {
      max-width: 100%;
    }

  }
</style>
