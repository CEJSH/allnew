(this["webpackJsonpreact-for-beginners"]=this["webpackJsonpreact-for-beginners"]||[]).push([[0],{33:function(e,t,n){},34:function(e,t,n){"use strict";n.r(t);var r=n(0),c=n.n(r),s=n(16),i=n.n(s),a=n(9),j=n(2),o=n(8),u=n.n(o),d=n(11),b=n(15),h=n(1);var l=function(e){var t=e.id,n=e.coverImg,r=e.title,c=e.year,s=e.summary,i=e.genres;return Object(h.jsxs)("div",{children:[Object(h.jsx)("img",{src:n,alt:r}),Object(h.jsxs)("div",{children:[Object(h.jsx)("h2",{children:Object(h.jsx)(a.b,{to:"/movie/".concat(t),children:r})}),Object(h.jsx)("h3",{children:c}),Object(h.jsx)("p",{children:s}),Object(h.jsx)("ul",{children:i.map((function(e){return Object(h.jsx)("li",{children:e},e)}))})]})]})};var O=function(){var e=Object(r.useState)(!0),t=Object(b.a)(e,2),n=t[0],c=t[1],s=Object(r.useState)([]),i=Object(b.a)(s,2),a=i[0],j=i[1],o=function(){var e=Object(d.a)(u.a.mark((function e(){var t;return u.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("https://yts.mx/api/v2/list_movies.json?minimum_rating=8.8&sort_by=year");case 2:return e.next=4,e.sent.json();case 4:t=e.sent,j(t.data.movies),c(!1);case 7:case"end":return e.stop()}}),e)})));return function(){return e.apply(this,arguments)}}();return Object(r.useEffect)((function(){o()}),[]),Object(h.jsx)("div",{children:n?Object(h.jsx)("div",{children:Object(h.jsx)("span",{children:"Loading..."})}):Object(h.jsx)("div",{children:a.map((function(e){return Object(h.jsx)(l,{id:e.id,year:e.year,coverImg:e.medium_cover_image,title:e.title,summary:e.summary,genres:e.genres},e.id)}))})})};var x=function(){var e=Object(j.f)().id,t=function(){var t=Object(d.a)(u.a.mark((function t(){var n;return u.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,fetch("https://yts.mx/api/v2/movie_details.json?movie_id=".concat(e));case 2:return t.next=4,t.sent.json();case 4:n=t.sent,console.log(n);case 6:case"end":return t.stop()}}),t)})));return function(){return t.apply(this,arguments)}}();return Object(r.useEffect)((function(){t()}),[]),Object(h.jsx)("h1",{children:"Detail"})};var v=function(){return Object(h.jsx)(a.a,{children:Object(h.jsxs)(j.c,{children:[Object(h.jsx)(j.a,{path:"/movie/:id",children:Object(h.jsx)(x,{})}),Object(h.jsx)(j.a,{path:"/",children:Object(h.jsx)(O,{})})]})})};n(33);i.a.render(Object(h.jsx)(c.a.StrictMode,{children:Object(h.jsx)(v,{})}),document.getElementById("root"))}},[[34,1,2]]]);
//# sourceMappingURL=main.259e0d16.chunk.js.map