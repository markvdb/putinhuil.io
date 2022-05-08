<template>
  <div>
    <header-section></header-section>
    <main>
      <form-section></form-section>
      <info-section></info-section>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import HeaderSection from '../components/HeaderSection.vue'
import FormSection from '../components/FormSection.vue'
import InfoSection from '../components/InfoSection.vue'

export default {
  name: 'HomeView',
  components: {
    HeaderSection,
    FormSection,
    InfoSection
  }
}
</script>
