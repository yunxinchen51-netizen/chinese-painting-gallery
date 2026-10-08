<script setup>
import { ref, reactive, onMounted } from 'vue'
import galleryDesk from './assets/figma/f7335acdfebc88c2cc66e1d65a48b2bd 1.png'
import detailBackground from './assets/figma/703381535b14b0b99bac1dcb50cc3a8 1.png'
import oneRain from './assets/figma/671d10ee6c078c9b59d936d31d62e53c 2.png'
import cloudPeaks from './assets/figma/组件-1.png'
import clearStream from './assets/figma/组件-2.png'
import autumnForest from './assets/figma/组件-3.png'
import cardOne from './assets/figma/组件.png'
import cardTwo from './assets/figma/组件-1.png'
import cardThree from './assets/figma/组件-2.png'
import cardFour from './assets/figma/组件-3.png'
import galleryBack from './assets/figma/image 238.png'
import navLandscape from './assets/figma/Group 8.png'
import navBirds from './assets/figma/Group 6.png'
import navPeople from './assets/figma/Group 7.png'
import draftsBadge from './assets/figma/Group 4.png'
import publishedBadge from './assets/figma/Group 5.png'
import profileBadge from './assets/figma/Group 237494.png'
import newWorkBadge from './assets/figma/Group 9246.png'
import detailProfile from './assets/figma/Group 237489.png'
import detailMetaTitle from './assets/figma/detail-meta-title.png'
import detailMetaDescription from './assets/figma/detail-meta-description.png'
import detailMetaTags from './assets/figma/detail-meta-tags.png'
import detailMetaLocation from './assets/figma/detail-meta-location.png'
import aiCat from './assets/figma/Group 237486.png'
import aiLabel from './assets/figma/AI助手.png'
import detailPanel from './assets/figma/Group 9206.png'
import detailPaper from './assets/figma/Mask group.png'
import rollerTop from './assets/figma/image 419.png'
import rollerBottom from './assets/figma/image 418.png'
import originalBadge from './assets/figma/Group 237561.png'
import statsLikes from './assets/figma/stats-likes.png'
import statsComments from './assets/figma/stats-comments.png'
import statsSaves from './assets/figma/stats-saves.png'
import commentsLabel from './assets/figma/评论.png'
import commentLikeIcon from './assets/figma/comment-like.png'
import createBackground from './assets/create/703381535b14b0b99bac1dcb50cc3a8 1.png'
import createPanel from './assets/create/Group 237554.png'
import createCat from './assets/create/Group 237486.png'
import createAiLabel from './assets/create/AI助手.png'
import createBack from './assets/create/image 238.png'
import createUpload from './assets/create/Group 237562.png'
import createPublish from './assets/create/发布作品.png'
import createReference from './assets/create/编辑发布.png'

const page = ref('gallery')
const createForm = reactive({ title: '', description: '', location: '', statement: '', tags: [] })
const selectedImage = ref('')
const editMode = ref(false)
const layoutVersion = 2
const splitKeys = ['detail-title', 'detail-description', 'detail-tags', 'detail-location', 'original-badge', 'stats-likes', 'stats-comments', 'stats-saves']
const dragPositions = reactive(JSON.parse(localStorage.getItem('gallery-layout-positions') || '{}'))
const dragState = reactive({ key: '', startX: 0, startY: 0, originX: 0, originY: 0 })
const apiBase = (import.meta.env.VITE_API_BASE_URL || '/api').replace(/\/$/, '')
const designWidth = 1920
const getCanvasWidth = () => Math.min(window.innerWidth, designWidth)
const canvasWidth = ref(getCanvasWidth())
const layoutBaseWidth = ref(Number(dragPositions.__viewportWidth) || canvasWidth.value)

function dragStyle(key) {
  const p = dragPositions[key] || { x: 0, y: 0 }
  const scale = canvasWidth.value / layoutBaseWidth.value
  return { '--drag-x': `${p.x * scale}px`, '--drag-y': `${p.y * scale}px` }
}

function startDrag(event, key) {
  if (!editMode.value) return
  event.preventDefault()
  event.stopPropagation()
  const p = dragPositions[key] || { x: 0, y: 0 }
  dragState.key = key
  dragState.startX = event.clientX
  dragState.startY = event.clientY
  const scale = canvasWidth.value / layoutBaseWidth.value
  dragState.originX = p.x
  dragState.originY = p.y
  dragState.scale = scale
  event.currentTarget.setPointerCapture?.(event.pointerId)
}

function moveDrag(event) {
  if (!editMode.value || !dragState.key) return
  dragPositions[dragState.key] = {
    x: Math.round(dragState.originX + (event.clientX - dragState.startX) / dragState.scale),
    y: Math.round(dragState.originY + (event.clientY - dragState.startY) / dragState.scale),
  }
}

function endDrag() {
  if (!dragState.key) return
  persistLayout()
  dragState.key = ''
}

function persistLayout() {
  const positions = JSON.parse(JSON.stringify(dragPositions))
  positions.__viewportWidth = canvasWidth.value
  positions.__layoutVersion = layoutVersion
  layoutBaseWidth.value = canvasWidth.value
  // Keep a local copy for instant fallback, while the API is the shared source of truth.
  localStorage.setItem('gallery-layout-positions', JSON.stringify(positions))
  fetch(`${apiBase}/layout-positions/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ positions }),
  }).catch(() => {})
}

function toggleEditMode() {
  editMode.value = !editMode.value
  if (!editMode.value) endDrag()
}

onMounted(() => {
  window.addEventListener('pointermove', moveDrag)
  window.addEventListener('pointerup', endDrag)
  window.addEventListener('resize', () => { canvasWidth.value = getCanvasWidth() })
  fetch(`${apiBase}/layout-positions/`)
    .then((response) => {
      if (!response.ok) throw new Error('Unable to load shared layout')
      return response.json()
    })
    .then(({ positions }) => {
      if (!positions || typeof positions !== 'object') return
      const needsReset = positions.__layoutVersion !== layoutVersion
      if (needsReset) {
        splitKeys.forEach((key) => delete positions[key])
        positions.__layoutVersion = layoutVersion
      }
      layoutBaseWidth.value = Math.min(Number(positions.__viewportWidth) || canvasWidth.value, designWidth)
      const localPositions = JSON.parse(localStorage.getItem('gallery-layout-positions') || '{}')
      // One-time migration: preserve an existing local layout when the server is still empty.
      if (Object.keys(positions).length === 0 && Object.keys(localPositions).length > 0) {
        Object.assign(dragPositions, localPositions)
        persistLayout()
        return
      }
      Object.keys(dragPositions).forEach((key) => delete dragPositions[key])
      Object.assign(dragPositions, positions)
      localStorage.setItem('gallery-layout-positions', JSON.stringify(dragPositions))
      if (needsReset) persistLayout()
    })
    .catch(() => {})
})

const works = [
  { title: '一蓑烟雨', count: '1548', likes: '317', comments: '9', image: oneRain, cardImage: cardOne },
  { title: '云起峰峦', count: '758', likes: '58', comments: '16', image: cloudPeaks, cardImage: cardTwo },
  { title: '溪山清远', count: '172', likes: '32', comments: '5', image: clearStream, cardImage: cardThree },
  { title: '秋林晚照图', count: '1296', likes: '258', comments: '7', image: autumnForest, cardImage: cardFour },
]

const comments = [
  { text: '看到这幅画，我仿佛回到了儿时乡间小院，看着满园春色，听着燕子呢喃。楼阁和桃花的搭配让人感到静谧又生机勃勃，像是对故乡春日的一种深情呼唤。', likes: 3 },
  { text: '画中的楼阁和桃花，不禁让我联想到“桃花源记”中的意象——一个隔绝喧嚣的理想国。山水的虚实对比与传统中国画“气韵生动”的理念十分契合，体现了画家对传统文化的深刻理解。', likes: 1 },
  { text: '青山含雾，静水垂纶，笔墨悠然，尽得山水间闲适清逸之意。', likes: 1 },
  { text: '山间繁花掩映亭台，很容易让人想起古诗词里的春日山水。画面远近层次分明，虚实相生，一草一木皆有情，尽显传统山水画独有的诗意之美，可以看出画家深厚的笔墨功底。', likes: 1 },
]

function openDetail(work) {
  if (work.title !== '一蓑烟雨') return
  page.value = 'detail'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function backToGallery() {
  page.value = 'gallery'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openCreate() {
  page.value = 'create'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function backFromCreate() {
  page.value = 'gallery'
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function toggleCreateTag(tag) {
  createForm.tags = createForm.tags.includes(tag)
    ? createForm.tags.filter((item) => item !== tag)
    : [...createForm.tags, tag]
}

function chooseImage(event) {
  const file = event.target.files?.[0]
  if (!file) return
  selectedImage.value = URL.createObjectURL(file)
}
</script>

<template>
  <Transition name="dissolve" mode="out-in">
    <main v-if="page === 'gallery'" key="gallery" class="figma-page gallery-page" :class="{ 'layout-editing': editMode }" :style="{ backgroundImage: `url(${galleryDesk})` }">
      <button class="layout-toggle" @click="toggleEditMode">{{ editMode ? '完成调整' : '调整布局' }}</button>
      <header class="figma-header">
        <div class="brand draggable-part" :style="dragStyle('brand')" @pointerdown="startDrag($event, 'brand')"><img :src="galleryBack" alt="返回" /><strong>我的画廊</strong></div>
        <nav class="tabs draggable-part" :style="dragStyle('tabs')" @pointerdown="startDrag($event, 'tabs')"><button class="image-tab active"><img :src="navLandscape" alt="山水胜景" /></button><button class="image-tab"><img :src="navBirds" alt="花鸟灵犀" /></button><button class="image-tab"><img :src="navPeople" alt="人物风流" /></button></nav>
        <label class="search draggable-part" :style="dragStyle('search')" @pointerdown="startDrag($event, 'search')"><span>⌕</span><input placeholder="搜索画作、词牌..." /></label>
        <img class="profile-badge" :src="profileBadge" alt="用户等级" />
      </header>

      <section class="gallery-toolbar">
        <div class="gallery-tabs"><img :src="draftsBadge" alt="我的草稿 1/10" /><img :src="publishedBadge" alt="已发布 4/10" /></div>
      </section>

      <section class="card-grid" aria-label="我的画廊作品">
        <button v-for="work in works" :key="work.title" class="work-card" @click="openDetail(work)">
          <img class="card-export" :src="work.cardImage" :alt="work.title" />
        </button>
      </section>

      <button class="new-work" @click="openCreate"><img :src="newWorkBadge" alt="新建画作" /></button>
    </main>

    <main v-else-if="page === 'create'" key="create" class="figma-page create-page">
      <section class="create-reference-wrap">
        <img class="create-reference" :src="createReference" alt="发布作品页面" />
        <label class="create-upload" :class="{ 'has-image': selectedImage }">
          <img v-if="selectedImage" :src="selectedImage" alt="已选择的作品" />
          <img v-else :src="createUpload" alt="添加作品图片" />
          <input type="file" accept="image/*" @change="chooseImage" />
        </label>
        <input v-model="createForm.title" class="create-field create-title" aria-label="标题" placeholder="" />
        <textarea v-model="createForm.description" class="create-field create-description" aria-label="正文描述" placeholder="创作意图/色彩技巧运用..." />
        <input v-model="createForm.location" class="create-field create-location" aria-label="标记地点" />
        <div class="create-tags" aria-label="添加标签">
          <button v-for="tag in ['山水','花鸟','人物','写意']" :key="tag" :class="{ selected: createForm.tags.includes(tag) }" @click="toggleCreateTag(tag)">{{ tag }}</button>
        </div>
        <input v-model="createForm.statement" class="create-field create-statement" aria-label="自主声明" />
        <button class="create-back-hit" @click="backFromCreate" aria-label="返回"></button>
        <button class="create-save-hit" @click="backFromCreate" aria-label="保存"></button>
        <button class="create-publish-hit" @click="backFromCreate" aria-label="发布作品"></button>
      </section>
    </main>

    <main v-else-if="page === 'detail'" key="detail" class="figma-page detail-page" :class="{ 'layout-editing': editMode }" :style="{ backgroundImage: `url(${detailBackground})` }">
      <button class="layout-toggle" @click="toggleEditMode">{{ editMode ? '完成调整' : '调整布局' }}</button>
      <header class="figma-header detail-header">
        <button class="back" @click="backToGallery"><img :src="galleryBack" alt="返回" /><span>春山烟雨图</span></button>
        <div class="detail-tools draggable-part" :style="dragStyle('detail-tools')" @pointerdown="startDrag($event, 'detail-tools')"><img :src="aiCat" alt="AI助手" /><img :src="aiLabel" alt="AI助手" /></div>
      </header>

      <section class="detail-content">
        <div class="detail-left draggable-part" :style="dragStyle('detail-left')" @pointerdown="startDrag($event, 'detail-left')">
          <img class="roller roller-top" :src="rollerTop" alt="" />
          <img class="paper-frame" :src="detailPaper" alt="" />
          <img class="detail-art" :src="oneRain" alt="春山烟雨图" />
          <img class="original-badge draggable-part" :style="dragStyle('original-badge')" @pointerdown="startDrag($event, 'original-badge')" :src="originalBadge" alt="原创作品" />
          <div class="stats-piece stats-likes draggable-part" :style="dragStyle('stats-likes')" @pointerdown="startDrag($event, 'stats-likes')"><img :src="statsLikes" alt="点赞 317" /></div>
          <div class="stats-piece stats-comments draggable-part" :style="dragStyle('stats-comments')" @pointerdown="startDrag($event, 'stats-comments')"><img :src="statsComments" alt="评论 32" /></div>
          <div class="stats-piece stats-saves draggable-part" :style="dragStyle('stats-saves')" @pointerdown="startDrag($event, 'stats-saves')"><img :src="statsSaves" alt="收藏 9" /></div>
          <img class="roller roller-bottom" :src="rollerBottom" alt="" />
        </div>
        <section class="detail-side draggable-part" :style="dragStyle('detail-side')" @pointerdown="startDrag($event, 'detail-side')">
          <img class="side-panel" :src="detailPanel" alt="" />
          <img class="detail-profile" :src="detailProfile" alt="好学的皓皓" />
          <div class="meta-piece meta-title draggable-part" :style="dragStyle('detail-title')" @pointerdown="startDrag($event, 'detail-title')">
            <img :src="detailMetaTitle" alt="作品标题" />
          </div>
          <div class="meta-piece meta-description draggable-part" :style="dragStyle('detail-description')" @pointerdown="startDrag($event, 'detail-description')">
            <img :src="detailMetaDescription" alt="作品简介" />
          </div>
          <div class="meta-piece meta-tags draggable-part" :style="dragStyle('detail-tags')" @pointerdown="startDrag($event, 'detail-tags')">
            <img :src="detailMetaTags" alt="作品标签" />
          </div>
          <div class="meta-piece meta-location draggable-part" :style="dragStyle('detail-location')" @pointerdown="startDrag($event, 'detail-location')">
            <img :src="detailMetaLocation" alt="作品地点" />
          </div>
          <img class="comments-label-image" :src="commentsLabel" alt="评论" />
          <div class="comment-input">写下你的点评吧！</div>
          <div class="comment-list" aria-label="评论区">
            <article v-for="comment in comments" :key="comment.text" class="comment-card">
              <div class="comment-card-main">
                <div class="comment-avatar">👤</div>
                <p>{{ comment.text }}</p>
              </div>
              <div class="comment-card-footer">
                <span class="comment-stars" aria-label="5 星">★★★★★</span>
                <span class="comment-like"><img :src="commentLikeIcon" alt="" />{{ comment.likes }}</span>
              </div>
            </article>
          </div>
        </section>
      </section>
    </main>
  </Transition>
</template>
