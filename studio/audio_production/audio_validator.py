class AudioValidator:
 def validate(self,timeline,mix):return [] if all(c.end>=c.start for c in timeline.clips) else ["Audio clip has invalid timing"]
