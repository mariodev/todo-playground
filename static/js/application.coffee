# coffee --watch --compile application.coffee
class @Todo extends Backbone.Model

	defaults:
		type: 'pending'

	url: ->
		u = "/api/todos"
		u += "/#{@get('_id')}" unless @isNew()
		return u

	isNew: ->
		!@get('_id')?

	validate: (attrs) ->
		if !attrs.content? or attrs.content.trim() is ""
			return message: "Title can't be blank."


class @Todos extends Backbone.Collection
	model: Todo
	url: "/api/todos"


class @TodoListView extends Backbone.View
	el: '#todos'

	initialize: ->
		@collection.bind('reset', @render)
		@collection.fetch()
		@collection.bind('add', @renderAdded)
		new NewTodoView(collection: @collection)

	render: =>
		@collection.forEach (todo) =>
			$(@el).append(new TodoListItemView(model: todo).el)

	renderAdded: (todo) =>
		$("#new_todo").after(new TodoListItemView(model: todo).el)


class @TodoListItemView extends Backbone.View
	tagName: 'li'
	events:
		'keypress .todo_title': 'handleKeypress'
		'change .todo_state': 'saveModel'
		'click .btn-danger': 'destroy'

	initialize: ->
		@template = _.template($('#todo_template').html())
		@model.bind('change', @render)
		@model.bind('error', @modelSaveFailed)
		@render()

	render: =>
		$(@el).html(@template(@model.toJSON()))
		if @model.get('type') is 'completed'
			@$('.todo_state').attr('checked', true)
			@$('label.active').removeClass('active')
			@$('.todo_title').addClass('completed').attr('disabled', true)
		return @

	handleKeypress: (e) =>
		if e.keyCode is 13
			@saveModel(e)

	saveModel: (e) =>
		e?.preventDefault()
		attrs = {content: @$('.todo_title').val()}
		if @$('.todo_state').attr('checked')?
			attrs.type = 'completed'
		else
			attrs.type = 'pending'
		@model.save attrs

	modelSaveFailed: (model, error) =>
		if error.responseText?
			error = JSON.parse(error.responseText)
		alert error.message
		@$('.todo_title').val(@model.get('content'))

	destroy: (e) =>
		e?.preventDefault()
		if confirm "Are You sure?"
			@model.destroy
				success: =>
					$(@el).remove()


class @NewTodoView extends Backbone.View
	el: '#new_todo'
	events:
		'keypress .todo_title': 'handleKeypress'

	initialize: ->
		@collection.bind('add', @resetForm)
		@$('.todo_title').focus()

	handleKeypress: (e) =>
		if e.keyCode is 13
			@saveModel(e)

	resetForm: (todo) =>
		@$('.todo_title').val('')

	saveModel: (e) =>
		e?.preventDefault()
		model = new Todo()
		model.save {content: @$('.todo_title').val()},
			success: =>
				@collection.add(model)
			error: (model, error) =>
				# console.log error
				if error.responseText?
					error = JSON.parse(error.responseText)
				alert error.message


$ ->
	new TodoListView(collection: new Todos())
