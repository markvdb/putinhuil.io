<template>
  <div>
    <header-section></header-section>
    <main>
      <form-section></form-section>
      <info-section></info-section>
      <info-section-2></info-section-2>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src
import HeaderSection from '../components/HeaderSection.vue'
import FormSection from '../components/FormSection.vue'
import InfoSection from '../components/InfoSection.vue'
import InfoSection2 from '@/components/InfoSection2.vue'

export default {
  name: 'HomeView',
  components: {
    HeaderSection,
    FormSection,
    InfoSection,
    InfoSection2
  }
}
</script>
