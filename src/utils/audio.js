const TARGET_SAMPLE_RATE = 16000

const writeAscii = (view, offset, text) => {
  for (let i = 0; i < text.length; i++) {
    view.setUint8(offset + i, text.charCodeAt(i))
  }
}

const encodeWav16BitMono = (samples, sampleRate) => {
  const bytesPerSample = 2
  const buffer = new ArrayBuffer(44 + samples.length * bytesPerSample)
  const view = new DataView(buffer)

  writeAscii(view, 0, 'RIFF')
  view.setUint32(4, 36 + samples.length * bytesPerSample, true)
  writeAscii(view, 8, 'WAVE')
  writeAscii(view, 12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)
  view.setUint16(22, 1, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * bytesPerSample, true)
  view.setUint16(32, bytesPerSample, true)
  view.setUint16(34, 16, true)
  writeAscii(view, 36, 'data')
  view.setUint32(40, samples.length * bytesPerSample, true)

  let offset = 44
  for (let i = 0; i < samples.length; i++) {
    const normalized = Math.max(-1, Math.min(1, samples[i]))
    const pcm = normalized < 0 ? normalized * 0x8000 : normalized * 0x7fff
    view.setInt16(offset, pcm, true)
    offset += 2
  }

  return new Blob([buffer], { type: 'audio/wav' })
}

const toMono = (audioBuffer) => {
  if (audioBuffer.numberOfChannels === 1) {
    return audioBuffer.getChannelData(0)
  }

  const mono = new Float32Array(audioBuffer.length)
  for (let ch = 0; ch < audioBuffer.numberOfChannels; ch++) {
    const channelData = audioBuffer.getChannelData(ch)
    for (let i = 0; i < audioBuffer.length; i++) {
      mono[i] += channelData[i]
    }
  }

  for (let i = 0; i < mono.length; i++) {
    mono[i] /= audioBuffer.numberOfChannels
  }

  return mono
}

export const convertBlobToPcmWav16kMono = async (recordedBlob) => {
  const AudioContextCtor = window.AudioContext || window.webkitAudioContext
  const ctx = new AudioContextCtor()

  try {
    const sourceBuffer = await recordedBlob.arrayBuffer()
    const decoded = await ctx.decodeAudioData(sourceBuffer.slice(0))
    const monoSamples = toMono(decoded)

    const outLength = Math.ceil(monoSamples.length * TARGET_SAMPLE_RATE / decoded.sampleRate)
    const offlineCtx = new OfflineAudioContext(1, outLength, TARGET_SAMPLE_RATE)
    const workBuffer = offlineCtx.createBuffer(1, monoSamples.length, decoded.sampleRate)
    workBuffer.copyToChannel(monoSamples, 0)

    const node = offlineCtx.createBufferSource()
    node.buffer = workBuffer
    node.connect(offlineCtx.destination)
    node.start(0)

    const rendered = await offlineCtx.startRendering()
    return encodeWav16BitMono(rendered.getChannelData(0), TARGET_SAMPLE_RATE)
  } finally {
    await ctx.close().catch(() => {})
  }
}
